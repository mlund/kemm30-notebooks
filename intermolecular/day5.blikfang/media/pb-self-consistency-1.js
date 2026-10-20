// A damped Poisson/Boltzmann fixed-point iteration. Animation is numerical, not time dynamics.
const C = r => blikfang.colour(r);
const W=1440,H=680,N=40,ld=30.4,L=120/ld,h=L/N,thermal=25.7,mix=.30;
let potential=Array.from({length:N+1},(_,i)=>1-i/N);
let ionPhi=Array(N+1).fill(0), phase='ions', rounds=0, playing=false, busy=false;
const svg=d3.select(el).append('svg').attr('viewBox',`0 0 ${W} ${H}`).attr('width','100%').attr('height','100%').style('display','block').style('font-family','inherit');
const label=(x,y,t,size=26,anchor='start')=>svg.append('text').attr('x',x).attr('y',y).attr('fill',C('text')).attr('font-size',size).attr('text-anchor',anchor).text(t);
const line=(x1,y1,x2,y2,col='text',width=3)=>svg.append('line').attr('x1',x1).attr('y1',y1).attr('x2',x2).attr('y2',y2).attr('stroke',C(col)).attr('stroke-width',width);
const arrow=(points,col='accent')=>{
 svg.append('path').attr('d',d3.line()(points)).attr('stroke',C(col)).attr('stroke-width',4).attr('fill','none');
 const [a,b]=points.slice(-2), angle=Math.atan2(b[1]-a[1],b[0]-a[0]);
 const p=[b,[b[0]-15*Math.cos(angle-.45),b[1]-15*Math.sin(angle-.45)],[b[0]-15*Math.cos(angle+.45),b[1]-15*Math.sin(angle+.45)]];
 svg.append('path').attr('d',d3.line()(p)+'Z').attr('fill',C(col));
};
label(90,50,'Potential guess',32);label(900,50,'Ion distribution',32);
arrow([[405,40],[835,40]]);label(620,28,'Boltzmann',25,'middle');
const status=label(720,108,'Start: guessed potential, uniform ions.',27,'middle');
const x=d3.scaleLinear([0,120],[115,625]), y=d3.scaleLinear([0,28],[440,160]);
svg.append('g').attr('transform','translate(0,440)').call(d3.axisBottom(x).ticks(4)).attr('font-size',24);
svg.append('g').attr('transform','translate(115,0)').call(d3.axisLeft(y).ticks(4)).attr('font-size',24);
label(370,505,'Distance from wall (Å)',25,'middle');
label(43,300,'Potential (mV)',25,'middle').attr('transform','rotate(-90,43,300)');
line(108,155,108,445,'orange',5);
for(let yy=180;yy<440;yy+=60)label(92,yy,'+',25,'middle').attr('fill',C('orange'));
const path=d3.line().x((v,i)=>x(i*120/N)).y(v=>y(v*thermal));
const oldCurve=svg.append('path').attr('fill','none').attr('stroke',C('faint')).attr('stroke-width',3).attr('stroke-dasharray','8 6');
const curve=svg.append('path').attr('fill','none').attr('stroke',C('purple')).attr('stroke-width',5);
label(130,550,'Solid: current potential; dashed: previous guess',23);
// Fixed candidate positions; opacity supplies smooth, illustrative changes in populations.
const ions=svg.append('g');
const particles=[];
for(let bin=0;bin<10;bin++){
 const xx=bin*120/9;
 for(const sign of [-1,1]) for(let k=0;k<9;k++){
  particles.push({bin,xx,sign,k,cx:828+bin*53+(k%2)*20,cy:(sign<0?195:365)+Math.floor(k/2)*26});
 }
}
label(815,160,'Negative ions (counterions)',25).attr('fill',C('blue'));
label(815,338,'Positive ions (co-ions)',25).attr('fill',C('orange'));
line(802,175,802,490,'orange',5);
for(let yy=200;yy<490;yy+=60)label(785,yy,'+',25,'middle').attr('fill',C('orange'));
const dots=ions.selectAll('g').data(particles).join('g').attr('transform',d=>`translate(${d.cx},${d.cy})`);
dots.append('circle').attr('r',11).attr('fill',d=>C(d.sign<0?'blue':'orange'));
dots.append('text').attr('text-anchor','middle').attr('dy','.34em').attr('font-size',21).attr('fill',C('background')).text(d=>d.sign<0?'−':'+');
label(815,510,'wall',23);label(1325,510,'reservoir',23,'end');
label(815,550,'Symbols illustrate concentration, not trajectories.',23);
arrow([[1140,565],[1140,590],[370,590],[370,565]]);
svg.append('rect').attr('x',570).attr('y',570).attr('width',455).attr('height',38).attr('fill',C('background'));
label(790,596,'Poisson: ionic charge sets curvature',25,'middle');
const counter=label(1325,651,'Round 0',24,'end');
function sample(a,xx){const t=xx*N/120,i=Math.min(N-1,Math.floor(t));return a[i]+(a[i+1]-a[i])*(t-i);}
function draw(p,ip){
 curve.attr('d',path(p));
 dots.attr('opacity',d=>{
  const number=3*Math.exp(-d.sign*sample(ip,d.xx));
  return .08+.92*Math.max(0,Math.min(1,number-d.k));
 });
}
function solvePoisson(ip){
 // Dirichlet endpoints Φ(0)=1 and Φ(120 Å)=0. Thomas algorithm for -Φ''=-sinh(Φ_ions).
 const n=N-1,c=Array(n).fill(0),v=Array(n).fill(0);
 for(let j=0;j<n;j++){
  let rhs=-h*h*Math.sinh(ip[j+1]);if(j===0)rhs+=1;
  const den=2+(j?c[j-1]:0);
  c[j]=-1/den;v[j]=(rhs+(j?v[j-1]:0))/den;
 }
 const out=Array(N+1).fill(0);out[0]=1;
 for(let j=n-1;j>=0;j--)out[j+1]=v[j]-c[j]*out[j+2];
 return out;
}
function button(x0,width,text,action){
 const g=svg.append('g').attr('transform',`translate(${x0},620)`).attr('role','button').attr('tabindex',0).attr('aria-label',text).style('cursor','pointer');
 g.append('rect').attr('width',width).attr('height',48).attr('rx',9).attr('fill',C('surface')).attr('stroke',C('accent')).attr('stroke-width',2);
 const t=g.append('text').attr('x',width/2).attr('y',32).attr('text-anchor','middle').attr('font-size',25).attr('fill',C('text')).text(text);
 g.on('click',action).on('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();action();}});
 return t;
}
function setPlayLabel(value){playText.text(value);d3.select(playText.node().parentNode).attr('aria-label',value);}
function pause(){playing=false;setPlayLabel('Play');svg.interrupt('pb-loop');busy=false;draw(potential,ionPhi);}
function advance(){
 if(busy||!el.isConnected)return;
 busy=true;
 const isIons=phase==='ions',a=potential.slice(),b=ionPhi.slice();
 const raw=isIons?null:solvePoisson(ionPhi);
 const target=isIons?a:a.map((v,i)=>(i===0||i===N)?v:v+mix*(raw[i]-v));
 const change=isIons?0:d3.max(target.map((v,i)=>Math.abs(v-a[i])));
 status.text(isIons?'Boltzmann: calculate ions from this potential.':'Poisson: revise potential using this ionic charge.');
 if(!isIons)oldCurve.attr('d',path(a));
 const duration=playing?(isIons?1400:1700):850;
 svg.transition('pb-loop').duration(duration).ease(d3.easeCubicInOut).tween('profiles',()=>t=>{
  if(!el.isConnected){playing=false;svg.interrupt('pb-loop');return;}
  if(isIons){ionPhi=b.map((v,i)=>v+t*(target[i]-v));draw(potential,ionPhi);}
  else{potential=a.map((v,i)=>v+t*(target[i]-v));draw(potential,ionPhi);}
 }).on('end',()=>{
  busy=false;
  if(isIons){ionPhi=target.slice();phase='potential';status.text('Ions match the guess. Now let their charge revise it.');}
  else{
   potential=target.slice();rounds++;phase='ions';counter.text('Round '+rounds);
   status.text('Potential changed. Recalculate the ions, then repeat.');
   if(change<.0001){
    ionPhi=potential.slice();draw(potential,ionPhi);playing=false;setPlayLabel('Play');
    status.text('Self-consistent: ions and potential agree. This is PB equilibrium.');return;
   }
  }
  draw(potential,ionPhi);
  if(playing&&el.isConnected)advance();
 });
}
const playText=button(90,150,'Play',()=>{if(playing){pause();return;}playing=true;setPlayLabel('Pause');advance();});
button(265,180,'Single step',()=>{if(playing)pause();if(!busy)advance();});
button(470,150,'Restart',()=>{
 pause();potential=Array.from({length:N+1},(_,i)=>1-i/N);ionPhi=Array(N+1).fill(0);rounds=0;phase='ions';
 oldCurve.attr('d',null);counter.text('Round 0');status.text('Start: guessed potential, uniform ions.');draw(potential,ionPhi);
});
draw(potential,ionPhi);
