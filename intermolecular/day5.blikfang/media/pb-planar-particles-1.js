// Quantile transport illustrates equilibrium population updates; it is not ion dynamics.
const C=r=>blikfang.colour(r), W=1440,H=720,N=40,thermal=25.7,ld=30.4,L=120/ld,h=L/N,mix=.30;
const baseCount=70,poolCount=160, xLeft=140,xRight=1120,yTop=115,yBottom=300;
let potential=Array.from({length:N+1},(_,i)=>1-i/N),ionPhi=Array(N+1).fill(0);
let phase='ions',rounds=0,playing=false,busy=false,sliceX=Math.max(6,Math.min(114,blikfang.get('slice_x')??35));
const svg=d3.select(el).append('svg').attr('viewBox',`0 0 ${W} ${H}`).attr('width','100%').attr('height','100%').style('display','block').style('font-family','inherit');
const label=(x,y,t,size=26,anchor='start')=>svg.append('text').attr('x',x).attr('y',y).attr('fill',C('text')).attr('font-size',size).attr('text-anchor',anchor).text(t);
const x=d3.scaleLinear([0,120],[xLeft,xRight]),py=d3.scaleLinear([0,28],[575,435]);
const frac=n=>n-Math.floor(n);
// Stable random-looking samples: independent coordinates, never a lattice or redraw noise.
function scatter(seed){
 let n=(seed+0x9e3779b9)>>>0;
 n=Math.imul(n^(n>>>16),0x21f0aaad);
 n=Math.imul(n^(n>>>15),0x735a2d97);
 return ((n^(n>>>15))>>>0)/4294967296;
}
const status=label(720,72,'Start: uniform ions and a guessed potential.',28,'middle');
label(140,30,'Positive wall',28);
svg.append('circle').attr('cx',635).attr('cy',22).attr('r',9).attr('fill',C('red'));
label(654,30,'+ cations',25);
svg.append('circle').attr('cx',825).attr('cy',22).attr('r',9).attr('fill',C('green'));
label(844,30,'− anions',25);
label(1284,98,'Reservoir',25,'middle');
svg.append('rect').attr('x',1170).attr('y',110).attr('width',230).attr('height',200).attr('rx',12).attr('fill',C('surface')).attr('stroke',C('line'));
// The reservoir symbols are contextual; mobile particles are drawn in a separate layer.
for(let i=0;i<12;i++)svg.append('circle').attr('cx',1188+scatter(12001+i)*192).attr('cy',130+scatter(13001+i)*160).attr('r',6).attr('fill',C(i%2?'green':'red')).attr('opacity',.45);
svg.append('line').attr('x1',1170).attr('x2',1170).attr('y1',110).attr('y2',310).attr('stroke',C('line')).attr('stroke-dasharray','6 5');
svg.append('rect').attr('x',113).attr('y',105).attr('width',13).attr('height',210).attr('fill',C('red'));
for(let yy=135;yy<310;yy+=42)label(99,yy,'+',27,'middle').attr('fill',C('red'));
const sliceTop=svg.append('rect').attr('y',105).attr('height',210).attr('fill',C('accent')).attr('fill-opacity',.08).attr('stroke',C('accent')).attr('stroke-width',2);
const guides=svg.append('g');
const guideLeft=guides.append('line'),guideRight=guides.append('line');
for(const g of [guideLeft,guideRight])g.attr('y1',315).attr('y2',430).attr('stroke',C('accent')).attr('stroke-width',1.5).attr('stroke-dasharray','5 5').attr('opacity',.45);
const sliceBottom=svg.append('rect').attr('y',430).attr('height',150).attr('fill',C('accent')).attr('fill-opacity',.08).attr('stroke',C('accent')).attr('stroke-width',1.5);
const particles=[];
for(const sign of [1,-1])for(let j=0;j<poolCount;j++)particles.push({sign,j,y:yTop+12+scatter(j*3+(sign>0?211:911))*(yBottom-yTop-24)});
const dots=svg.append('g').selectAll('circle').data(particles).join('circle').attr('r',6).attr('fill',d=>C(d.sign>0?'red':'green')).attr('stroke',C('background')).attr('stroke-width',.7);
label(1172,353,'Ions can enter / leave.',22);
label(1172,417,'Selected slice',26);
const slicePositive=label(1180,457,'',26).attr('fill',C('red'));
const sliceNegative=label(1180,494,'',26).attr('fill',C('green'));
const sliceNet=label(1180,535,'',25);
const sliceWhere=label(1180,574,'',23);
svg.append('g').attr('transform','translate(0,575)').call(d3.axisBottom(x).ticks(6)).attr('font-size',24);
svg.append('g').attr('transform',`translate(${xLeft},0)`).call(d3.axisLeft(py).ticks(3)).attr('font-size',24);
label(44,505,'Potential (mV)',25,'middle').attr('transform','rotate(-90,44,505)');
label(630,630,'Distance x from the plane (Å)',25,'middle');
const curveFn=d3.line().x((v,i)=>x(i*120/N)).y(v=>py(v*thermal));
const oldCurve=svg.append('path').attr('fill','none').attr('stroke',C('faint')).attr('stroke-width',3).attr('stroke-dasharray','7 6');
const curve=svg.append('path').attr('fill','none').attr('stroke',C('purple')).attr('stroke-width',4);
const curveDot=svg.append('circle').attr('r',6).attr('fill',C('purple')).attr('stroke',C('background'));
label(142,417,'Potential: solid = current; dashed = previous guess',23);
svg.append('line').attr('x1',xLeft).attr('x2',xRight).attr('y1',374).attr('y2',374).attr('stroke',C('line')).attr('stroke-width',2);
const handle=svg.append('circle').attr('cy',374).attr('r',12).attr('fill',C('accent')).attr('stroke',C('text')).attr('role','slider').attr('tabindex',0).attr('aria-label','Slice distance in angstroms').attr('aria-valuemin',6).attr('aria-valuemax',114).style('cursor','ew-resize');
const sliceLabel=label(0,349,'',25,'middle');
function sample(a,z){const t=z*N/120,i=Math.min(N-1,Math.max(0,Math.floor(t)));return a[i]+(a[i+1]-a[i])*(t-i);}
function positions(ip){
 const result=[];
 for(const sign of [1,-1]){
  const density=ip.map(v=>Math.exp(-sign*v)),cdf=[0];
  for(let i=1;i<=N;i++)cdf.push(cdf[i-1]+.5*(density[i-1]+density[i])/N);
  const mass=cdf[N],number=baseCount*mass;
  for(let j=0;j<poolCount;j++){
   // One jittered quantile per rank retains the concentration profile without visible columns.
   const offset=.08+.84*scatter(j+(sign>0?1337:7331));
   const q=(j+offset)/number;
   if(q>=1){result.push({x:1260+frac(j*.43)*90,opacity:0});continue;}
   const target=q*mass;let k=1;while(k<N&&cdf[k]<target)k++;
   const f=(target-cdf[k-1])/(cdf[k]-cdf[k-1]);
   result.push({x:x((k-1+f)*120/N),opacity:1});
  }
 }
 return result;
}
let pointPositions=positions(ionPhi);
function updateSlice(){
 const left=x(sliceX-6),right=x(sliceX+6);
 for(const r of [sliceTop,sliceBottom])r.attr('x',left).attr('width',right-left);
 guideLeft.attr('x1',left).attr('x2',left);guideRight.attr('x1',right).attr('x2',right);
 handle.attr('cx',x(sliceX)).attr('aria-valuenow',Math.round(sliceX));
 sliceLabel.attr('x',x(sliceX)).text('Drag slice: x = '+Math.round(sliceX)+' Å');
 const counts={positive:0,negative:0};
 pointPositions.forEach((p,i)=>{if(p.opacity>.5&&p.x>=left&&p.x<right)counts[particles[i].sign>0?'positive':'negative']++;});
 slicePositive.text('+ ions: '+counts.positive);sliceNegative.text('− ions: '+counts.negative);
 const net=counts.positive-counts.negative;
 sliceNet.text(net===0?'Net: neutral':net<0?'Net: negative':'Net: positive').attr('fill',C(net===0?'text':net<0?'green':'red'));
 sliceWhere.text('Slice width: 12 Å');
 curveDot.attr('cx',x(sliceX)).attr('cy',py(thermal*sample(potential,sliceX)));
}
function draw(){
 dots.attr('cx',(d,i)=>pointPositions[i].x).attr('cy',d=>d.y).attr('opacity',(d,i)=>pointPositions[i].opacity);
 curve.attr('d',curveFn(potential));updateSlice();
}
function moveSlice(z){sliceX=Math.max(6,Math.min(114,z));blikfang.set('slice_x',sliceX);updateSlice();}
handle.call(d3.drag().on('start',e=>e.sourceEvent?.stopPropagation()).on('drag',e=>moveSlice(x.invert(e.x))));
handle.on('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();e.stopPropagation();moveSlice(sliceX+(e.key==='ArrowRight'?5:-5));}});
blikfang.on('slice_x',z=>{sliceX=Math.max(6,Math.min(114,z));updateSlice();});
function solvePoisson(ip){
 const n=N-1,c=Array(n).fill(0),v=Array(n).fill(0);
 for(let j=0;j<n;j++){let rhs=-h*h*Math.sinh(ip[j+1]);if(j===0)rhs+=1;const den=2+(j?c[j-1]:0);c[j]=-1/den;v[j]=(rhs+(j?v[j-1]:0))/den;}
 const out=Array(N+1).fill(0);out[0]=1;for(let j=n-1;j>=0;j--)out[j+1]=v[j]-c[j]*out[j+2];return out;
}
function button(x0,w,title,action){
 const g=svg.append('g').attr('transform',`translate(${x0},655)`).attr('role','button').attr('tabindex',0).attr('aria-label',title).style('cursor','pointer');
 g.append('rect').attr('width',w).attr('height',48).attr('rx',8).attr('fill',C('surface')).attr('stroke',C('accent')).attr('stroke-width',2);
 const t=g.append('text').attr('x',w/2).attr('y',32).attr('text-anchor','middle').attr('fill',C('text')).attr('font-size',25).text(title);
 g.on('click',action).on('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();e.stopPropagation();action();}});return t;
}
function playLabel(v){playText.text(v);d3.select(playText.node().parentNode).attr('aria-label',v);}
function pause(){playing=false;playLabel('Play');svg.interrupt('pb-particles');busy=false;draw();}
function advance(){
 if(busy||!el.isConnected)return;busy=true;
 const isIons=phase==='ions',a=potential.slice(),b=ionPhi.slice(),from=pointPositions.map(p=>({...p}));
 const raw=isIons?null:solvePoisson(ionPhi),target=isIons?a:a.map((v,i)=>i===0||i===N?v:v+mix*(raw[i]-v));
 const to=isIons?positions(target):null;
 const change=isIons?0:d3.max(target.map((v,i)=>Math.abs(v-a[i])));
 status.text(isIons?'1 · The wall potential enriches − ions and depletes + ions.':'2 · Ionic charge changes the curvature of the potential.');
 if(!isIons)oldCurve.attr('d',curveFn(a));
 svg.transition('pb-particles').duration(isIons?2200:1600).ease(d3.easeCubicInOut).tween('motion',()=>t=>{
  if(!el.isConnected){playing=false;svg.interrupt('pb-particles');return;}
  if(isIons){
   ionPhi=b.map((v,i)=>v+t*(target[i]-v));
   pointPositions=from.map((v,i)=>({x:v.x+t*(to[i].x-v.x),opacity:v.opacity+t*(to[i].opacity-v.opacity)}));
  }else potential=a.map((v,i)=>v+t*(target[i]-v));
  draw();
 }).on('end',()=>{
  busy=false;
  if(isIons){ionPhi=target.slice();pointPositions=to;phase='potential';status.text('Ions have redistributed. Their charge now revises the potential.');}
  else{
   potential=target.slice();rounds++;roundLabel.text('Round '+rounds);phase='ions';status.text('New potential → recalculate the ion distribution.');
   if(change<.0001){ionPhi=potential.slice();pointPositions=positions(ionPhi);draw();playing=false;playLabel('Play');status.text('Self-consistent equilibrium: ions and potential agree.');return;}
  }
  draw();if(playing&&el.isConnected)advance();
 });
}
const playText=button(140,150,'Play',()=>{if(playing){pause();return;}playing=true;playLabel('Pause');advance();});
button(315,185,'Single step',()=>{if(playing)pause();if(!busy)advance();});
button(525,150,'Restart',()=>{pause();potential=Array.from({length:N+1},(_,i)=>1-i/N);ionPhi=Array(N+1).fill(0);pointPositions=positions(ionPhi);phase='ions';rounds=0;oldCurve.attr('d',null);roundLabel.text('Round 0');status.text('Start: uniform ions and a guessed potential.');draw();});
const roundLabel=label(1280,687,'Round 0',25,'middle');
draw();
