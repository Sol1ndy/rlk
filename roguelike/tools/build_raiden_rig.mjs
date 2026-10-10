// Original articulated puppet rig for Magatsu Mitake Narukami no Mikoto.
// The supplied skin is copied byte-for-byte. Geometry and all animation keys are authored here.
// node tools/build_raiden_rig.mjs --datapack <pack> --resourcepack <pack> --skin <provided PNG>
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const arg=n=>{const i=process.argv.indexOf(n);return i<0?null:process.argv[i+1];};
const dp=path.resolve(arg('--datapack')||path.join(here,'..'));
const rp=path.resolve(arg('--resourcepack'));
const assets=path.join(rp,'assets/rlk');
const put=(p,s)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,s.endsWith('\n')?s:s+'\n');};
const json=(p,o)=>put(p,JSON.stringify(o,null,2));
const fn=(n,s)=>put(path.join(dp,'data/rlk/function/boss/raiden/rig',n+'.mcfunction'),Array.isArray(s)?s.join('\n'):s);
const textures={skin:'rlk:raiden/skin',white:'rlk:player_motion/white_concrete',silver:'rlk:player_motion/light_gray_concrete',dark:'rlk:player_motion/black_concrete',purple:'rlk:player_motion/purple_concrete',blue:'rlk:player_motion/blue_concrete',light:'rlk:player_motion/light_blue_concrete',gold:'rlk:cm/fm/metal',deathGlow:'rlk:raiden/fx/lavender',deathViolet:'rlk:raiden/fx/violet_dense',deathWhite:'rlk:raiden/fx/white'};
const faces=['north','south','east','west','up','down'];
const box=(from,to,tex,overrides={})=>({from,to,faces:Object.fromEntries(faces.map(f=>[f,{texture:'#'+(overrides[f]||tex),uv:[0,0,16,16]}]))});
const model=(name,elements)=>{const trail=name.includes('_trail_'),fx=name.startsWith('fx_weapon/')?{purple:'rlk:raiden/fx/'+(trail?'afterglow':'violet_dense'),blue:'rlk:raiden/fx/void',light:'rlk:raiden/fx/cyan',white:'rlk:raiden/fx/'+(trail?'lavender':'white'),silver:'rlk:raiden/fx/lavender'}:{};json(path.join(assets,'models/item/raiden',name+'.json'),{ambientocclusion:false,textures:{...textures,...fx,particle:textures.purple},elements});json(path.join(assets,'items/raiden',name+'.json'),{model:{type:'minecraft:model',model:'rlk:item/raiden/'+name}});};
function skinFaces(u,v,w,h,d,start=0,end=h){const face=(a,b,c,e)=>({uv:[a/4,b/4,c/4,e/4],texture:'#skin'});return{east:face(u,v+d+start,u+d,v+d+end),north:face(u+d,v+d+start,u+d+w,v+d+end),west:face(u+d+w,v+d+start,u+2*d+w,v+d+end),south:face(u+2*d+w,v+d+start,u+2*d+2*w,v+d+end),up:face(u+d,v,u+d+w,v+d),down:face(u+d+w,v+d,u+d+2*w,v)};}
const sb=(a,b,uv,start,end,inflate=0)=>({from:a.map(v=>v-inflate),to:b.map(v=>v+inflate),faces:skinFaces(...uv,start,end)});
const bodySpecs={
 head:[[4,8,4],[12,16,12],[0,0,8,8,8],[32,0,8,8,8],0,8,.45],
 body:[[4,-4,6],[12,8,10],[16,16,8,12,4],[16,32,8,12,4],0,12,.22],
 right_arm:[[6,4,6],[10,10,10],[40,16,4,12,4],[40,32,4,12,4],0,6,.22],
 right_forearm:[[6,2,6],[10,8,10],[40,16,4,12,4],[40,32,4,12,4],6,12,.22],
 left_arm:[[6,4,6],[10,10,10],[32,48,4,12,4],[48,48,4,12,4],0,6,.22],
 left_forearm:[[6,2,6],[10,8,10],[32,48,4,12,4],[48,48,4,12,4],6,12,.22],
 right_leg:[[6,2,6],[10,8,10],[0,16,4,12,4],[0,32,4,12,4],0,6,.22],
 right_shin:[[6,2,6],[10,8,10],[0,16,4,12,4],[0,32,4,12,4],6,12,.22],
 left_leg:[[6,2,6],[10,8,10],[16,48,4,12,4],[0,48,4,12,4],0,6,.22],
 left_shin:[[6,2,6],[10,8,10],[16,48,4,12,4],[0,48,4,12,4],6,12,.22]
};
for(const[n,[a,b,uv,over,start,end,inf]]of Object.entries(bodySpecs))model(n,[sb(a,b,uv,start,end),sb(a,b,over,start,end,inf)]);
if(arg('--skin')){fs.mkdirSync(path.join(assets,'textures/raiden'),{recursive:true});fs.copyFileSync(arg('--skin'),path.join(assets,'textures/raiden/skin.png'));}

// All pieces remain within the native model cube bounds. Larger forms use display transforms.
const eye=(cx,cy,cz,size=1)=>[box([cx-2.4*size,cy-.5*size,cz],[cx+2.4*size,cy+.5*size,cz+.25],'gold'),box([cx-1.4*size,cy-1.05*size,cz+.05],[cx+1.4*size,cy+1.05*size,cz+.32],'white'),box([cx-.45*size,cy-1.2*size,cz+.1],[cx+.45*size,cy+1.2*size,cz+.4],'purple')];
const upper=[box([5.8,-4,5.8],[10.2,8,10.2],'purple'),box([5.25,-2.6,5.25],[10.75,6.4,10.75],'white',{east:'silver',south:'silver'}),box([5.05,5.3,5.05],[10.95,6.3,10.95],'gold'),box([5.05,-2.5,5.05],[10.95,-1.5,10.95],'gold'),box([5.6,6.5,5.6],[10.4,9.2,10.4],'dark'),...eye(8,2,4.93,.85)];
model('puppet_upper',upper);
model('puppet_forearm',[box([5.8,-6,5.8],[10.2,8,10.2],'purple'),box([5.3,-4.8,5.3],[10.7,5.9,10.7],'white',{east:'silver',south:'silver'}),box([5,4.7,5],[11,5.8,11],'gold'),box([5,-4.8,5],[11,-3.8,11],'gold'),box([6.7,-3.5,5.1],[9.3,4.9,5.3],'purple'),box([7.55,-3.4,4.98],[8.45,4.8,5.32],'light'),...eye(8,.3,4.8,.6)]);
function hand(closed){const e=[box([4.2,1.8,6.4],[11.8,8.3,9.6],'white',{south:'silver'}),box([4.4,6.9,6.1],[11.6,8.3,9.9],'gold'),box([5.3,2.8,6.15],[10.7,6.9,6.4],'purple'),...eye(8,4.8,6.01,.72)];for(let i=0;i<4;i++){const x=4.55+i*1.85;if(closed){e.push(box([x,-.5,6.25],[x+1.45,2.5,10.35],'white'),box([x,-.5,9.5],[x+1.45,3.3,11.0],'silver'),box([x,-.8,6],[x+1.45,.1,7],'purple'));}else{const end=[-3.7,-5,-4.6,-3.1][i];e.push(box([x,end,6.6],[x+1.4,2.2,9.1],'white',{east:'silver'}),box([x,end+1.1,6.45],[x+1.4,end+1.7,9.22],'gold'),box([x,end-.5,6.7],[x+1.4,end+.5,9],'purple'));}}e.push(box([2.5,2.0,6.7],[4.7,6.7,9.2],'white'),box([1.7,closed?1.3:.1,7.1],[3.6,3.8,9.4],'silver'));return e;}
model('puppet_hand_open',hand(false));model('puppet_hand_closed',hand(true));

// Curved violet cutting edge, bright silver spine, stepped point and gilded lotus guard.
function katana(big=false){const e=[box([7.3,1.8,7.25],[8.7,10,8.75],'dark'),box([7.05,2,7.05],[8.95,2.75,8.95],'gold')];for(let y=3;y<9;y+=1.55)e.push(box([7.12,y,7.12],[8.88,y+.62,8.88],'purple'));e.push(box([4.4,9.0,6.75],[11.6,10.15,9.25],'gold'),box([6,8.8,6.2],[10,10.3,9.8],'purple'));for(let i=0;i<14;i++){const y=10+i*1.51,curve=i*i*.0065,width=1.65-i*.075;e.push(box([7.9+curve-width/2,y,7.5],[7.9+curve+width/2,y+1.61,8.5],'purple',{north:'light',east:'white',south:big?'light':'blue'}),box([7.88+curve-width/2,y,7.43],[8.10+curve-width/2,y+1.62,8.57],'white'));}return e;}
model('katana',katana());model('giant_katana',katana(true));
// Lightning is geometry, not a particle cloud. Its white seam protrudes through
// the front/back of the violet body so the opaque shell never hides the core.
// Every blade attachment shares the actual weapon's hand pivot and quaternion.
function lightningLine(elements,points,outer,inner,trail=false){
 for(let j=1;j<points.length;j++){
  const a=points[j-1],b=points[j],steps=Math.max(1,Math.ceil(Math.hypot(...b.map((x,i)=>x-a[i]))/.55));
  for(let i=0;i<=steps;i++){
   const c=a.map((x,k)=>x+(b[k]-x)*i/steps);
   elements.push(box([c[0]-outer/2,c[1]-outer/2,c[2]-.24],[c[0]+outer/2,c[1]+outer/2,c[2]+.24],'purple'));
   elements.push(box([c[0]-inner/2,c[1]-inner/2,c[2]-.34],[c[0]+inner/2,c[1]+inner/2,c[2]+.34],'white'));
  }
 }
}
function bladeLightning(spear=false,variant=0,trail=false){
 const e=[],start=spear?17.8:10.2,end=30.5;
 for(const side of[-1,1]){
  const pts=[];for(let i=0;i<8;i++){
   const y=start+(end-start)*i/7,curve=spear?Math.pow((y-18)/1.65,2)*.025:Math.pow((y-10)/1.51,2)*.0065;
   pts.push([8+curve+side*(.95+(i%2===variant?1.10:.1)),y,8+side*.78]);
  }
  lightningLine(e,pts,trail?.62:1.02,trail?.2:.36,trail);
  for(const i of[2,5]){
   const c=pts[i],sign=side*(variant?1:-1);
   lightningLine(e,[c,[c[0]+side*1.6,c[1]+.8,c[2]+sign*.55],[c[0]+side*2.1,c[1]+2.5,c[2]+sign*.9]],trail?.4:.64,trail?.12:.2,trail);
  }
 }
 return e;
}
for(const kind of['katana','polearm'])for(const variant of[0,1]){
 model(`fx_weapon/${kind}_${variant}`,bladeLightning(kind==='polearm',variant));
 model(`fx_weapon/${kind}_trail_${variant}`,bladeLightning(kind==='polearm',variant,true));
}
// Open palm negative-Y fingers, with a sparse charged seal on the outside of
// the palm. The centre stays empty: readable hands rather than a glowing ball.
function palmLightning(closed=false,stage='charge',variant=0){
 const release=stage==='release',focus=stage==='focus',e=[],tips=closed?[.25,.1,.1,.45]:[-3.7,-5,-4.6,-3.1];
 for(let i=0;i<4;i++){
  const x=5.1+i*1.85,y=tips[i],bend=(i%2===variant?1:-1)*.6;
  lightningLine(e,[[x,y,6.0],[x+bend,y+1.1,5.8],[x-.15,2.5,5.6],[8+(i-1.5)*(focus?.2:.55),4.15,5.25]],release?.65:focus?.58:.46,release?.25:focus?.23:.16);
  if(release)lightningLine(e,[[x,y,6.0],[x+bend*1.8,y-1.25,5.7],[x-bend*.8,y-3.4,5.15],[x+bend*2.3,y-5.4,4.65]],.76,.27);
 }
 const radius=release?5.8:focus?1.15:2.2;
 for(let i=0;i<12;i++){
  const a=i*Math.PI/6,b=(i+1)*Math.PI/6,r=radius+(i%2===variant?.45:-.15);
  // The release becomes a broken expanding crown of sparks, not a solid disk.
  if(release&&i%3===1)continue;
  lightningLine(e,[[8+Math.cos(a)*r,3.8+Math.sin(a)*r,5.35],[8+Math.cos((a+b)/2)*(r+.4),3.8+Math.sin((a+b)/2)*(r+.4),4.9],[8+Math.cos(b)*r,3.8+Math.sin(b)*r,5.35]],release?.72:.42,release?.25:.14);
 }
 return e;
}
for(const form of['open','closed'])for(const phase of['charge','focus','release'])for(const variant of[0,1])model(`fx_weapon/palm_${form}_${phase}_${variant}`,palmLightning(form==='closed',phase,variant));
function chakraLightning(variant){
 const e=[];
 for(let i=0;i<6;i++){
  const a=(i*2+variant)*Math.PI/6,r=14.3;
  const p=(angle,radius,z)=>[8+Math.cos(angle)*radius,8+Math.sin(angle)*radius,z];
  lightningLine(e,[p(a-.12,r,7.2),p(a-.04,16.6,6.9),p(a+.035,15.8,7.1),p(a+.11,19.5,6.5)],.68,.22);
  lightningLine(e,[p(a-.04,16.6,6.9),p(a-.17,18.6,7.3),p(a-.20,20.4,7.6)],.46,.15);
  lightningLine(e,[p(a-.12,r,7.2),p(a-.25,14.8,7.2),p(a-.36,13.7,7.2)],.5,.17);
 }
 return e;
}
for(const variant of[0,1])model(`fx_weapon/chakra_${variant}`,chakraLightning(variant));
const spear=[box([7.4,-15.5,7.4],[8.6,18.2,8.6],'dark')];for(const y of[-12,-5,2,9,16])spear.push(box([7.16,y,7.16],[8.84,y+.7,8.84],'gold'));for(let i=0;i<8;i++){const y=18+i*1.65,w=2.2-i*.24,x=8+i*i*.025;spear.push(box([x-w/2,y,7.45],[x+w/2,y+1.72,8.55],'purple',{north:'light',east:'white'}));}spear.push(box([5.6,16,6.8],[10.4,18,9.2],'gold'),box([6.5,-15.8,6.5],[9.5,-14.6,9.5],'purple'));model('polearm',spear);

const ring=[];for(let i=0;i<64;i++){const a=i*Math.PI/32,x=8+13.6*Math.cos(a),y=8+13.6*Math.sin(a);ring.push(box([x-.75,y-.75,7.4],[x+.75,y+.75,8.6],i%8===0?'gold':'purple'));if(i%2===0)ring.push(box([8+12.3*Math.cos(a)-.42,8+12.3*Math.sin(a)-.42,7.65],[8+12.3*Math.cos(a)+.42,8+12.3*Math.sin(a)+.42,8.35],'light'));}for(let i=0;i<12;i++){const a=i*Math.PI/6,x=8+16*Math.cos(a),y=8+16*Math.sin(a);ring.push(box([x-.65,y-1.5,7.8],[x+.65,y+1.5,8.2],i%3===0?'gold':'purple'));}for(let l=0;l<3;l++){const a=l*Math.PI*2/3;for(let i=0;i<8;i++){const b=a+i*.16,x=8+6.2*Math.cos(b),y=8+6.2*Math.sin(b);ring.push(box([x-.6,y-.6,7.6],[x+.6,y+.6,8.4],'purple'));}}model('chakra',ring);
model('armor',[box([3.5,5.7,5.4],[12.5,8.1,10.6],'white'),box([3.3,5.2,5.2],[12.7,6.15,10.8],'gold'),box([5.1,-4.1,5.5],[10.9,-2,10.5],'purple'),box([4.4,-3.9,5.25],[11.6,-3,10.75],'gold'),box([6.85,1,5.1],[9.15,6.0,5.45],'white'),...eye(8,3.2,5.0,.7),box([3.2,-7.0,7],[5.3,-2.9,10.3],'purple'),box([10.7,-7,7],[12.8,-2.9,10.3],'purple')]);
model('crown',[box([3.65,12,3.75],[12.35,13.1,12.25],'gold'),box([3,13,5.2],[4.2,18.8,7.4],'purple'),box([2.7,17.6,5.1],[4.5,19.3,7.5],'white'),box([11.8,13,5.2],[13,18.8,7.4],'purple'),box([11.5,17.6,5.1],[13.3,19.3,7.5],'white'),...eye(8,13.3,3.5,.9)]);
model('ribbon',[box([6.4,-9,8.2],[9.6,8,9.15],'purple',{north:'blue'}),box([6.4,-9,8.1],[7.0,8,9.25],'gold'),box([9.0,-9,8.1],[9.6,8,9.25],'gold'),box([6.1,-11,8.2],[9.9,-8,9.15],'purple')]);
model('electro_orb',[box([4.5,12,4.5],[11.5,19,11.5],'purple'),box([5.2,12.7,3.9],[10.8,18.3,12.1],'light'),box([3.9,12.7,5.2],[12.1,18.3,10.8],'light'),box([6.7,10.9,6.7],[9.3,20.1,9.3],'white'),box([-.8,14.9,6.8],[3.5,16.1,9.2],'gold'),box([12.5,14.9,6.8],[16.8,16.1,9.2],'gold'),box([6.8,14.9,-.8],[9.2,16.1,3.5],'purple'),box([6.8,14.9,12.5],[9.2,16.1,16.8],'purple')]);
const flower=[box([4.5,8,4.5],[11.5,9.5,11.5],'gold'),box([6,9.5,6],[10,17,10],'purple'),box([6.6,13,6.6],[9.4,19.8,9.4],'light')];for(let i=0;i<6;i++){const a=i*Math.PI/3;for(let s=0;s<4;s++){const r=3+s*1.5,x=8+Math.cos(a)*r,z=8+Math.sin(a)*r,y=13+s*.85;flower.push(box([x-1.4,y-.6,z-1.4],[x+1.4,y+1.4,z+1.4],s===3?'white':s%2?'silver':'purple'));}}model('remembrance_flower',flower);
const stake=[box([3.2,8,3.2],[12.8,9.3,12.8],'dark'),box([4.0,9.3,4.0],[12,10.5,12],'gold'),box([5.6,10.4,5.6],[10.4,26,10.4],'purple'),box([6.6,10.8,5.2],[9.4,25.2,10.8],'light'),box([6.3,26,6.3],[9.7,28.6,9.7],'white'),box([7.2,28.6,7.2],[8.8,30.5,8.8],'light')];model('lightning_stake',stake);
// Static illusion retains the original full skin, origin at waist (place feet+1).
const illusion=[];const illParts=[[[4,16,4],[12,24,12],[0,0,8,8,8],[32,0,8,8,8],.4],[[4,4,6],[12,16,10],[16,16,8,12,4],[16,32,8,12,4],.2],[[0,4,6],[4,16,10],[40,16,4,12,4],[40,32,4,12,4],.2],[[12,4,6],[16,16,10],[32,48,4,12,4],[48,48,4,12,4],.2],[[4,-8,6],[8,4,10],[0,16,4,12,4],[0,32,4,12,4],.2],[[8,-8,6],[12,4,10],[16,48,4,12,4],[0,48,4,12,4],.2]];for(const[a,b,uv,over,inf]of illParts)illusion.push(sb(a,b,uv,0,uv[3]),sb(a,b,over,0,over[3],inf));model('illusion',illusion);

const zeros=[0,0,0],rad=d=>d*Math.PI/180;
function mul(a,b){const[x,y,z,w]=a,[X,Y,Z,W]=b;return[w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W,w*W-x*X-y*Y-z*Z];}
function q(e=zeros){const[x,y,z]=e.map(v=>rad(v)/2);return mul(mul([0,0,Math.sin(z),Math.cos(z)],[0,Math.sin(y),0,Math.cos(y)]),[Math.sin(x),0,0,Math.cos(x)]);}
const rot=(Q,v)=>mul(mul(Q,[...v,0]),[-Q[0],-Q[1],-Q[2],Q[3]]).slice(0,3),add=(a,b)=>a.map((x,i)=>x+b[i]),sub=(a,b)=>a.map((x,i)=>x-b[i]),times=(v,s)=>v.map(x=>x*s),lerp=(a,b,t)=>a.map((x,i)=>x+(b[i]-x)*t);
function aimDown(v){const len=Math.hypot(...v),n=times(v,1/Math.max(len,.0001));if(n[1]>.9999)return[1,0,0,0];const a=[-n[2],0,n[0],1-n[1]],m=Math.hypot(...a);return a.map(x=>x/m);}
const defaults={shift:[0,0,0],root:[0,0,0],torso:[0,0,0],head:[0,0,0],right_arm:[8,-8,-12],right_elbow:[16,0,0],left_arm:[5,0,9],left_elbow:[8,0,0],right_leg:[0,0,-2],right_knee:[0,0,0],left_leg:[0,0,2],left_knee:[0,0,0],weapon:[-18,0,0],ring:[0,0,0],form:[1],fade:[1],
 main_r_sh:[-.78,2.95,.65],main_r_el:[-1.8,3.65,.42],main_r_wr:[-2.05,2.45,-.5],main_r_hand:[0,0,-15],
 main_l_sh:[.78,2.5,.65],main_l_el:[1.85,1.6,.48],main_l_wr:[.36,1.07,-.15],main_l_hand:[90,0,0],
 rear_r_sh:[-.55,2.6,.92],rear_r_el:[-1.5,2.35,.6],rear_r_wr:[-1.35,2.15,-.2],rear_r_hand:[20,0,-18],
 rear_l_sh:[.55,2.75,.92],rear_l_el:[1.45,3.03,.48],rear_l_wr:[1.56,3.65,-.05],rear_l_hand:[150,0,22],giant_weapon:[-12,0,-15]};
const key=(tick,pose)=>({tick,pose});
// Forward is authored -Z: a negative torso pitch bows the chest toward the knees.
// One knee rests low while the opposite foot carries the weight for the recovery.
const kneeling={shift:[0,-.25,-.025],root:[0,0,0],torso:[-34,0,3],head:[-20,0,-3],right_arm:[45,0,-14],right_elbow:[12,0,0],left_arm:[68,4,16],left_elbow:[34,0,0],right_leg:[52,0,-5],right_knee:[-104,0,0],left_leg:[5,0,5],left_knee:[-93,0,0],weapon:[-76,-10,15],form:[0],fade:[1]};
const clips=[
 {id:0,name:'idle',length:40,loop:true,keys:[key(0,{}),key(20,{shift:[0,.035,0],head:[-2,0,0],left_arm:[7,0,11],main_r_wr:[-2.04,2.50,-.5],rear_l_wr:[1.53,3.69,-.02],ring:[0,0,4]}),key(40,{shift:[0,0,0],head:[0,0,0],left_arm:defaults.left_arm,main_r_wr:defaults.main_r_wr,rear_l_wr:defaults.rear_l_wr,ring:[0,0,0]})]},
 {id:1,name:'walk',length:24,loop:true,keys:[key(0,{right_leg:[23,0,-3],left_leg:[-23,0,3],right_arm:[-8,0,-12],left_arm:[22,0,10],weapon:[0,0,0]}),key(6,{shift:[0,.06,0],right_knee:[-20,0,0],left_knee:[-8,0,0]}),key(12,{right_leg:[-23,0,-3],left_leg:[23,0,3],right_arm:[20,0,-12],left_arm:[-14,0,10],right_knee:[0,0,0],left_knee:[0,0,0],shift:[0,0,0]}),key(18,{shift:[0,.06,0],right_knee:[-8,0,0],left_knee:[-20,0,0]}),key(24,{right_leg:[23,0,-3],left_leg:[-23,0,3],right_arm:[-8,0,-12],left_arm:[22,0,10],right_knee:[0,0,0],left_knee:[0,0,0],shift:[0,0,0]})]},
 {id:2,name:'slash_wind',length:18,keys:[key(0,{}),key(10,{torso:[-4,-36,-6],right_arm:[65,-35,-75],right_elbow:[32,0,0],left_arm:[18,10,33],left_elbow:[25,0,0],weapon:[-70,8,85],right_leg:[-8,0,-7],left_leg:[12,0,5],main_r_wr:[-2.55,3.65,.15],giant_weapon:[-25,-25,65]}),key(18,{torso:[-5,-42,-8],right_arm:[70,-40,-80],right_elbow:[35,0,0],weapon:[-76,8,85]})]},
 {id:3,name:'slash_a',length:12,keys:[key(0,{torso:[-4,-40,-7],right_arm:[70,-40,-80],right_elbow:[35,0,0],weapon:[-76,8,85],main_r_wr:[-2.55,3.65,.15],giant_weapon:[-25,-25,65]}),key(4,{torso:[10,28,8],right_arm:[88,55,-15],right_elbow:[8,0,0],weapon:[-20,85,90],left_arm:[-12,-10,40],main_r_wr:[.4,2.25,-2.25],main_r_el:[-1.1,3.3,-1.2],giant_weapon:[-78,20,68]}),key(8,{torso:[8,40,12],right_arm:[70,74,10],weapon:[-15,85,90],main_r_wr:[1.45,1.75,-1.5],giant_weapon:[-70,25,100]}),key(12,{torso:[3,20,5],right_arm:[35,35,-10],weapon:[-35,15,45],main_r_wr:[.8,2.15,-1.2]})]},
 {id:4,name:'slash_b',length:12,keys:[key(0,{torso:[4,32,8],right_arm:[70,70,0],weapon:[-25,30,85],main_r_wr:[1.45,2,-1.5],giant_weapon:[-70,25,100]}),key(4,{torso:[8,-35,-7],right_arm:[95,-58,-44],weapon:[-55,-30,-78],left_arm:[-15,0,32],main_r_wr:[-2.3,2.3,-1.8],main_r_el:[-1.8,3.5,-1.2],giant_weapon:[-80,-30,-82]}),key(12,{torso:[0,-15,-2],right_arm:[28,-20,-15],weapon:[-20,0,-30]})]},
 {id:5,name:'thrust_wind',length:18,keys:[key(0,{}),key(12,{torso:[-4,-40,0],right_arm:[30,-42,-28],right_elbow:[68,0,0],left_arm:[36,10,25],left_elbow:[45,0,0],weapon:[-9,0,90],right_leg:[-16,0,-6],left_leg:[16,0,6],main_r_wr:[-1.65,2.6,.65],giant_weapon:[-88,0,0]}),key(18,{torso:[-6,-42,0]})]},
 {id:6,name:'thrust',length:14,keys:[key(0,{torso:[-4,-38,0],right_arm:[32,-40,-24],right_elbow:[60,0,0],weapon:[-4,0,90],main_r_wr:[-1.65,2.6,.65],giant_weapon:[-88,0,0]}),key(4,{shift:[0,0,-.18],torso:[18,10,0],right_arm:[90,4,-6],right_elbow:[2,0,0],weapon:[0,0,90],left_arm:[-22,-15,35],main_r_el:[-.9,2.85,-1.15],main_r_wr:[-.55,2.5,-2.35],giant_weapon:[-92,0,0]}),key(9,{shift:[0,0,-.1],torso:[8,0,0],right_arm:[78,2,-10]}),key(14,{shift:[0,0,0],torso:[0,0,0],right_arm:[24,0,-15],right_elbow:[10,0,0],weapon:[-10,0,0]})]},
 {id:7,name:'cast_wind',length:30,keys:[key(0,{}),key(12,{left_arm:[140,-15,35],left_elbow:[25,0,0],right_arm:[16,0,-16],head:[-13,-6,0],rear_l_wr:[1.3,4.3,-.4],rear_l_hand:[175,0,20],rear_r_wr:[-1.5,3.5,-.5],rear_r_hand:[150,0,-20],ring:[0,0,15]}),key(24,{left_arm:[157,-8,20],left_elbow:[12,0,0],head:[-18,0,0],rear_l_wr:[1.25,4.4,-.4],rear_r_wr:[-1.5,3.6,-.5],ring:[0,0,22]}),key(30,{left_arm:[160,-8,19]})]},
 {id:8,name:'cast',length:16,keys:[key(0,{left_arm:[160,-8,19],left_elbow:[12,0,0],rear_l_wr:[1.25,4.4,-.4],rear_r_wr:[-1.5,3.6,-.5]}),key(4,{torso:[10,0,0],left_arm:[92,-8,18],left_elbow:[2,0,0],rear_l_wr:[.85,2.7,-1.55],rear_r_wr:[-.85,2.7,-1.55],rear_l_hand:[75,0,0],rear_r_hand:[75,0,0]}),key(10,{torso:[5,0,0],left_arm:[78,-8,22]}),key(16,{left_arm:[30,-5,17],left_elbow:[10,0,0],torso:[0,0,0]})]},
 {id:9,name:'transform',length:70,keys:[key(0,{form:[0],torso:[18,0,0],head:[25,0,0],right_arm:[28,0,-12],left_arm:[28,0,12],right_elbow:[70,0,0],left_elbow:[70,0,0]}),key(16,{form:[.1],shift:[0,.1,0],torso:[-10,0,0],head:[-15,0,0],right_arm:[110,-10,-75],left_arm:[110,10,75],right_elbow:[25,0,0],left_elbow:[25,0,0],main_r_wr:[-1.2,2.3,.3],main_l_wr:[1.2,1.3,.3],ring:[0,0,-30]}),key(38,{form:[.75],shift:[0,.15,0],right_arm:[42,0,-45],left_arm:[42,0,45],right_leg:[28,0,-10],left_leg:[28,0,10],right_knee:[-55,0,0],left_knee:[-55,0,0],main_r_wr:[-2.5,3.2,-.5],main_l_wr:[.4,.9,-.15],giant_weapon:[-15,0,-50],ring:[0,0,10]}),key(56,{form:[1],shift:[0,0,0],torso:[0,0,0],head:[0,0,0],right_arm:[20,0,-16],left_arm:[20,0,16],right_elbow:[38,0,0],left_elbow:[38,0,0],main_r_wr:defaults.main_r_wr,main_l_wr:defaults.main_l_wr,giant_weapon:defaults.giant_weapon,ring:[0,0,0]}),key(70,{})]},
 {id:10,name:'arm_sweep_wind',length:30,keys:[key(0,{}),key(18,{torso:[-5,-30,-6],main_r_el:[-1.4,3.9,.7],main_r_wr:[-2.8,4.2,.15],giant_weapon:[-12,-20,75],rear_r_wr:[-1.65,3.1,.0],rear_r_hand:[90,0,-25],left_arm:[36,0,30],ring:[0,0,-10]}),key(30,{main_r_wr:[-2.95,4.25,.25],giant_weapon:[-10,-20,80]})]},
 {id:11,name:'arm_sweep',length:16,keys:[key(0,{torso:[-5,-30,-6],main_r_el:[-1.4,3.9,.7],main_r_wr:[-2.95,4.25,.25],giant_weapon:[-10,-20,80]}),key(4,{torso:[10,15,4],main_r_el:[-1.0,3.0,-1.6],main_r_wr:[0,2.5,-3.0],giant_weapon:[-85,20,85],rear_r_wr:[-.7,2.35,-1.5]}),key(8,{torso:[8,35,10],main_r_el:[-.3,2.8,-1.4],main_r_wr:[2.4,1.65,-1.3],giant_weapon:[-95,20,95]}),key(16,{torso:[0,10,0],main_r_el:defaults.main_r_el,main_r_wr:[-1.5,2.3,-1.2],giant_weapon:[-40,0,15]})]},
 {id:12,name:'clap_wind',length:32,keys:[key(0,{}),key(18,{main_r_el:[-2.0,3.1,.3],main_r_wr:[-3.05,2.35,-.55],main_r_hand:[90,0,-90],main_l_el:[2,3.1,.3],main_l_wr:[3.05,2.35,-.55],main_l_hand:[90,0,90],rear_r_wr:[-.9,3.9,-.1],rear_l_wr:[.9,3.9,-.1],left_arm:[38,0,32],right_arm:[38,0,-32],giant_weapon:[0,0,-25]}),key(32,{main_r_wr:[-3.25,2.45,-.65],main_l_wr:[3.25,2.45,-.65]})]},
 {id:13,name:'clap',length:16,keys:[key(0,{main_r_el:[-2,3.1,.3],main_r_wr:[-3.25,2.45,-.65],main_r_hand:[90,0,-90],main_l_el:[2,3.1,.3],main_l_wr:[3.25,2.45,-.65],main_l_hand:[90,0,90]}),key(4,{torso:[12,0,0],main_r_el:[-1.5,2.3,-1.2],main_r_wr:[-.28,1.65,-2.1],main_l_el:[1.5,2.3,-1.2],main_l_wr:[.28,1.65,-2.1],right_arm:[74,0,-12],left_arm:[74,0,12]}),key(8,{main_r_wr:[-.38,1.65,-2.1],main_l_wr:[.38,1.65,-2.1]}),key(16,{torso:[0,0,0],main_r_wr:[-1.3,2.1,-.7],main_l_wr:[1.3,1.65,-.7]})]},
 {id:14,name:'slam_wind',length:30,keys:[key(0,{}),key(18,{torso:[-15,0,0],head:[-18,0,0],main_l_el:[1.65,3.45,.1],main_l_wr:[1.1,4.8,-.45],main_l_hand:[175,0,15],rear_r_wr:[-1.1,4.2,-.2],rear_l_wr:[1.25,4.1,-.2],left_arm:[142,0,25],right_arm:[110,0,-25]}),key(30,{main_l_wr:[1.05,5.0,-.5]})]},
 {id:15,name:'slam',length:20,keys:[key(0,{main_l_el:[1.65,3.45,.1],main_l_wr:[1.05,5,-.5],main_l_hand:[175,0,15],torso:[-15,0,0]}),key(5,{torso:[30,0,0],head:[12,0,0],main_l_el:[1.3,1.3,-1.2],main_l_wr:[.7,.35,-2.1],main_l_hand:[65,0,10],rear_r_wr:[-1.1,.7,-1.2],rear_l_wr:[1.15,.7,-1.2],left_arm:[95,0,18],right_arm:[84,0,-22]}),key(10,{main_l_wr:[.7,.35,-2.1]}),key(20,{torso:[5,0,0],main_l_el:defaults.main_l_el,main_l_wr:defaults.main_l_wr,left_arm:[30,0,20]})]},
 {id:16,name:'judgment_wind',length:64,keys:[key(0,{}),key(18,{main_r_el:[-1.65,3.8,.3],main_r_wr:[-.75,4.7,-.4],giant_weapon:[0,0,0],main_l_wr:[.75,3.9,-.65],main_l_hand:[155,0,-25],rear_r_wr:[-.85,3.5,-.8],rear_l_wr:[.85,3.5,-.8],right_arm:[150,0,-14],left_arm:[130,0,15],head:[-20,0,0],ring:[0,0,-15]}),key(42,{main_r_wr:[-.25,5.1,-.3],main_l_wr:[.35,4.1,-.7],rear_r_wr:[-.55,3.85,-.75],rear_l_wr:[.55,3.85,-.75],right_arm:[170,0,-10],left_arm:[152,0,10],ring:[0,0,20]}),key(64,{main_r_wr:[-.25,5.25,-.3],ring:[0,0,40]})]},
 {id:17,name:'judgment',length:26,keys:[key(0,{main_r_el:[-1.65,3.8,.3],main_r_wr:[-.25,5.25,-.3],giant_weapon:[0,0,0],main_l_wr:[.35,4.1,-.7],head:[-20,0,0],right_arm:[170,0,-10],left_arm:[152,0,10]}),key(6,{torso:[32,0,0],head:[15,0,0],main_r_el:[-1.05,2.6,-1.25],main_r_wr:[-.2,1.0,-2.25],giant_weapon:[-135,0,0],main_l_wr:[.7,1.8,-1.7],rear_r_wr:[-1.6,1.3,-1.2],rear_l_wr:[1.6,1.3,-1.2],right_arm:[120,0,-10],left_arm:[85,0,20]}),key(13,{torso:[28,0,0],main_r_wr:[-.2,.85,-2.2],giant_weapon:[-150,0,0]}),key(26,{torso:[8,0,0],main_r_wr:[-1.1,2.1,-1.0],giant_weapon:[-65,0,-15],right_arm:[50,0,-15],left_arm:[35,0,20]})]},
 {id:18,name:'stagger',length:30,keys:[key(0,{}),key(4,{torso:[-23,0,-8],head:[-18,0,8],right_arm:[-15,10,-35],left_arm:[-15,-10,35],main_r_wr:[-2.35,2.3,.2],main_l_wr:[.7,.9,.2],rear_r_wr:[-1.7,2.2,.7],rear_l_wr:[1.7,2.9,.7]}),key(13,{torso:[25,0,3],head:[20,0,0],right_arm:[25,0,-12],left_arm:[25,0,12],right_knee:[-30,0,0],left_knee:[-30,0,0],shift:[0,-.15,0]}),key(30,{torso:[20,0,0],head:[18,0,0],shift:[0,-.18,0]})]},
 {id:19,name:'death',length:48,keys:[key(0,{form:[1]}),key(4,{shift:[0,.03,.03],torso:[18,-3,-7],head:[15,0,8],right_arm:[-8,0,-30],left_arm:[-12,0,34],right_elbow:[20,0,0],left_elbow:[16,0,0],main_r_wr:[-2.6,2.1,.25],main_l_wr:[1.5,1.05,.3],rear_r_wr:[-1.6,2.1,.4],rear_l_wr:[1.7,2.8,.5],form:[1]}),key(12,{shift:[0,-.22,-.025],torso:[-18,0,5],head:[-15,0,-4],right_arm:[30,0,-18],left_arm:[55,0,22],right_leg:[48,0,-7],right_knee:[-100,0,0],left_leg:[20,0,7],left_knee:[-90,0,0],main_r_wr:[-2.4,1.0,-.2],main_l_wr:[1.7,.45,-.3],rear_r_wr:[-1.8,1.3,.2],rear_l_wr:[1.75,1.8,.3],giant_weapon:[-105,0,-12],form:[.70]}),key(22,{...kneeling,shift:[0,-.27,-.04],torso:[-55,0,6],head:[-27,0,-4],right_arm:[44,0,-20],right_elbow:[18,0,0],left_arm:[74,0,24],left_elbow:[18,0,0],form:[.16]}),key(30,{shift:[0,-.32,-.07],torso:[-72,-6,8],head:[-24,0,-5],right_arm:[62,0,-24],right_elbow:[10,0,0],left_arm:[78,0,22],left_elbow:[8,0,0],form:[0],fade:[1]}),key(38,{shift:[0,-.32,-.07],torso:[-75,-6,8],fade:[.94]}),key(44,{shift:[0,-.15,-.07],fade:[.44]}),key(48,{shift:[0,.15,-.07],fade:[0]})]},
 {id:20,name:'spin',length:24,loop:true,keys:[key(0,{root:[0,0,0],right_arm:[80,0,-82],weapon:[-70,0,90],left_arm:[40,0,60],giant_weapon:[-75,0,90],main_r_wr:[-2.8,2.6,-.4]}),key(6,{root:[0,90,0],main_r_wr:[-2.6,2.7,-.5]}),key(12,{root:[0,180,0],main_r_wr:[-2.8,2.6,-.4]}),key(18,{root:[0,270,0],main_r_wr:[-2.6,2.7,-.5]}),key(24,{root:[0,360,0],main_r_wr:[-2.8,2.6,-.4]})]},
 {id:21,name:'dash',length:16,loop:true,keys:[key(0,{shift:[0,-.08,0],torso:[30,0,0],head:[-15,0,0],right_arm:[-38,-8,-16],left_arm:[-30,8,20],right_elbow:[10,0,0],left_elbow:[10,0,0],right_leg:[40,0,-5],left_leg:[-38,0,5],weapon:[-35,0,-20],main_r_wr:[-2,2.2,.8],giant_weapon:[-50,0,-30]}),key(8,{right_leg:[-38,0,-5],left_leg:[40,0,5],right_knee:[-30,0,0],left_knee:[-5,0,0]}),key(16,{right_leg:[40,0,-5],left_leg:[-38,0,5],right_knee:[-5,0,0],left_knee:[-30,0,0]})]},
 {id:22,name:'exhausted',length:60,loop:true,keys:[key(0,kneeling),key(30,{shift:[0,-.23,-.025],torso:[-31,0,3],head:[-17,0,-3],left_arm:[66,4,16]}),key(60,kneeling)]},
 {id:23,name:'collapse',length:46,keys:[key(0,{form:[1]}),key(4,{shift:[0,.025,.02],torso:[20,-5,-7],head:[16,0,8],right_arm:[-10,0,-28],left_arm:[-8,0,32],right_elbow:[20,0,0],left_elbow:[16,0,0],main_r_wr:[-2.5,2.5,.2],main_l_wr:[1.25,1.1,.1],rear_r_wr:[-1.6,2.15,.5],rear_l_wr:[1.7,2.9,.45],form:[1]}),key(11,{shift:[0,-.06,-.005],torso:[-10,0,5],head:[-5,0,-4],right_arm:[26,0,-18],left_arm:[40,0,22],right_leg:[28,0,-6],left_leg:[24,0,6],right_knee:[-55,0,0],left_knee:[-58,0,0],main_r_wr:[-2.3,1.8,-.15],main_l_wr:[1.4,.65,-.1],rear_r_wr:[-1.7,1.7,.4],rear_l_wr:[1.6,2.1,.3],giant_weapon:[-105,0,-15],form:[.88]}),key(20,{...kneeling,shift:[0,-.13,-.015],torso:[-42,0,5],head:[-25,0,-4],right_arm:[54,0,-16],left_arm:[72,4,20],form:[.30]}),key(30,{...kneeling,shift:[0,-.27,-.035],torso:[-43,0,4],head:[-24,0,-4],form:[0]}),key(38,{...kneeling,shift:[0,-.245,-.025],torso:[-32,0,3]}),key(46,kneeling)]},
 {id:24,name:'recover',length:28,keys:[key(0,kneeling),key(6,{shift:[0,-.26,-.02],torso:[-48,0,1],head:[-8,0,0],left_arm:[76,4,18],left_elbow:[18,0,0],right_arm:[43,0,-14],right_leg:[56,0,-5],right_knee:[-106,0,0],left_knee:[-98,0,0]}),key(14,{shift:[0,-.12,-.01],torso:[-25,0,0],head:[-3,0,0],right_leg:[28,0,-4],right_knee:[-55,0,0],left_leg:[12,0,4],left_knee:[-50,0,0],right_arm:[20,0,-12],left_arm:[46,4,15],left_elbow:[15,0,0]}),key(22,{shift:[0,0,0],torso:[-6,0,0],head:[0,0,0],right_leg:[5,0,-2],right_knee:[-10,0,0],left_leg:[5,0,2],left_knee:[-10,0,0],right_arm:[8,-8,-12],right_elbow:[16,0,0],left_arm:[10,0,10],left_elbow:[8,0,0]}),key(28,{shift:[0,0,0],torso:[0,0,0],head:[0,0,0],right_leg:[0,0,-2],right_knee:[0,0,0],left_leg:[0,0,2],left_knee:[0,0,0],left_arm:[5,0,9],form:[0]})]}
];
// Attacks accelerate into contact, hold only a brief impact beat, then recover.
// Controller contract: contact key 2 (+1 interpolation), heavy contact key 3 (+1).
const retime={
 1:[0,4,9,13,18],2:[0,4,6],3:[0,2,4,7],4:[0,2,7],
 5:[0,4,6],6:[0,2,5,9],7:[0,5,8,10],8:[0,2,5,9],
 9:[0,10,25,38,46],10:[0,5,8],11:[0,2,4,9],12:[0,5,8],
 13:[0,2,4,9],14:[0,5,8],15:[0,3,5,12],16:[0,6,10,14],
 17:[0,3,6,15],20:[0,3,6,9,12],21:[0,5,10]
};
for(const c of clips)if(retime[c.id]){c.keys.forEach((k,i)=>k.tick=retime[c.id][i]);c.length=c.keys.at(-1).tick;}
const hitTick=new Map([[3,2],[4,2],[6,2],[8,2],[11,2],[13,2],[15,3],[17,3]]);
const windIds=new Set([2,5,7,10,12,14,16]);
const fxNames=['weapon_fx','weapon_trail_1','weapon_trail_2','weapon_trail_3','giant_fx','giant_trail_1','giant_trail_2','giant_trail_3'];
const palmParts={palm_main_r:'main_r_hand',palm_main_l:'main_l_hand',palm_rear_r:'rear_r_hand',palm_rear_l:'rear_l_hand'};
const powerFxNames=[...Object.keys(palmParts),'palm_skin','chakra_fx'];
const pnames=[...Object.keys(bodySpecs),'weapon','armor','crown','ribbon_r','ribbon_l','chakra',...['main_r','main_l','rear_r','rear_l'].flatMap(n=>[n+'_upper',n+'_forearm',n+'_hand']),'giant_weapon',...fxNames,...powerFxNames];
function posed(p,phase,anim){
 let armor=phase===2?1:phase===1?p.form[0]:0;
 if(anim===23&&phase===3)armor=p.form[0];
 if(anim===19&&(phase===1||phase===2))armor=p.form[0];
 const form=armor*p.fade[0],bodyScale=(1.20+.38*form)*p.fade[0],lift=1.05*form,hip=add([0,.75,0],p.shift),root=q(p.root),body=q(p.torso),top=add(hip,rot(body,[0,.75,0])),o={body:{t:top,q:body},head:{t:top,q:mul(body,q(p.head))}};
 for(const[side,sign]of[['right',-1],['left',1]]){const sh=add(hip,rot(body,[sign*.375,.625,0])),arm=mul(body,q(p[side+'_arm'])),el=add(sh,rot(arm,[0,-.25,0])),fore=mul(arm,q(p[side+'_elbow'])),leg=q(p[side+'_leg']),pelvis=add(hip,[sign*.125,0,0]);o[side+'_arm']={t:sh,q:arm};o[side+'_forearm']={t:el,q:fore};o[side+'_leg']={t:pelvis,q:leg};o[side+'_shin']={t:add(pelvis,rot(leg,[0,-.375,0])),q:mul(leg,q(p[side+'_knee']))};if(side==='right'){
   // Blade +Y must point into the attack. Solve its final orientation in body
   // space while retaining the animated hand pivot; a hanging arm's -Y axis
   // must never silently reverse a spear thrust or turn a cut into a back strike.
   let blade=[-15,0,-15];
   if([2,3,4].includes(anim))blade=[-90,p.torso[1]*1.15,0];
   if([5,6].includes(anim))blade=[-90,p.torso[1]*.35,0];
   if(anim===20)blade=[-90,-70,0];
   if(anim===21)blade=[-18,0,-28];
   if([19,22,23].includes(anim))blade=[-80,-10,15];
   if(anim===24){const u=Math.max(0,Math.min(1,-p.torso[0]/34));blade=[-15-65*u,-10*u,-15+30*u];}
   o.weapon={t:add(el,rot(fore,[0,-.31,0])),q:q(blade),s:[1.12,1.12,1.12]};
 }}
 o.armor={t:top,q:body,s:[form,form,form]};o.crown={...o.head,s:[form,form,form]};o.ribbon_r={t:add(top,rot(body,[-.2,-.38,.25])),q:mul(body,q([12,0,-8]))};o.ribbon_l={t:add(top,rot(body,[.2,-.38,.25])),q:mul(body,q([8,0,8]))};
 for(const v of Object.values(o)){v.t=add(hip,rot(root,sub(v.t,hip)));v.q=mul(root,v.q);v.t=add(times(v.t,bodyScale),[0,lift,0]);v.s=times(v.s||[1,1,1],bodyScale);}
 if(form>.01)o.weapon.s=[0,0,0];
 const auxSize={main_r:1.55,main_l:1.85,rear_r:.95,rear_l:.95};
 for(const n of['main_r','main_l','rear_r','rear_l']){const sh=p[n+'_sh'],el=p[n+'_el'],wr=p[n+'_wr'];for(const[part,a,b,base]of[['upper',sh,el,.75],['forearm',el,wr,.875]]){const delta=sub(b,a);o[n+'_'+part]={t:a,q:aimDown(delta),s:[auxSize[n]*form,Math.hypot(...delta)/base*form,auxSize[n]*form]};}o[n+'_hand']={t:wr,q:q(p[n+'_hand']),s:Array(3).fill(auxSize[n]*form)};}
 o.giant_weapon={t:add(p.main_r_wr,[0,-.2,0]),q:q(p.giant_weapon),s:Array(3).fill(2.15*form)};
 if([12,13,15,19].includes(anim))o.giant_weapon.s=[0,0,0];
 o.chakra={t:[0,3.28,1.05],q:q(p.ring),s:Array(3).fill(1.65*form)};
 for(const n of pnames.filter(n=>n.startsWith('main_')||n.startsWith('rear_')||['chakra','giant_weapon'].includes(n))){const v=o[n];v.t=add([0,2,0],rot(root,sub(v.t,[0,2,0])));v.q=mul(root,v.q);}
 for(const v of Object.values(o)){v.t=[v.t[0],v.t[1],-v.t[2]];v.q=[-v.q[0],-v.q[1],v.q[2],v.q[3]];}
 return o;
}
const f=x=>(Math.abs(x)<.0000005?0:x).toFixed(6)+'f',arr=a=>'['+a.map(f).join(',')+']';
const nbt=v=>`{translation:${arr(v.t)},left_rotation:${arr(v.q)},scale:${arr(v.s||[1,1,1])},right_rotation:[0f,0f,0f,1f]}`;
function modelFor(n,anim=0){
 if(n==='chakra_fx')return'fx_weapon/chakra_0';
 if(n.startsWith('palm_'))return palmModel(n,anim,false,0);
 if(fxNames.includes(n)){const kind=n.startsWith('weapon')&&[5,6].includes(anim)?'polearm':'katana';return'fx_weapon/'+kind+(n.includes('trail')?'_trail':'')+'_0';}
 if(n==='weapon')return[5,6].includes(anim)?'polearm':'katana';if(n==='giant_weapon')return'giant_katana';if(n.endsWith('_upper'))return'puppet_upper';if(n.endsWith('_forearm')&&!Object.hasOwn(bodySpecs,n))return'puppet_forearm';if(n.endsWith('_hand'))return(n==='main_r_hand'&&![12,13].includes(anim))||(n==='main_l_hand'&&[14,15].includes(anim))?'puppet_hand_closed':'puppet_hand_open';if(n.startsWith('ribbon_'))return'ribbon';return n;
}
function palmModel(n,anim,release,variant){
 const closed=(n==='palm_main_r'&&![12,13].includes(anim))||(n==='palm_main_l'&&[14,15].includes(anim));
 return`fx_weapon/palm_${closed?'closed':'open'}_${release==='focus'?'focus':release?'release':'charge'}_${variant}`;
}
function sample(clip,t){let prev=structuredClone(defaults);const ks=clip.keys.map(k=>{prev={...prev,...k.pose};return{tick:k.tick,p:structuredClone(prev)};});let a=ks[0],b=a;for(const k of ks){if(k.tick<=t)a=k;else{b=k;break;}b=a;}const u=a.tick===b.tick?0:(t-a.tick)/(b.tick-a.tick),contact=hitTick.get(clip.id),smooth=contact!==undefined&&b.tick===contact?u*u:contact!==undefined&&a.tick>=contact?1-(1-u)*(1-u):u*u*(3-2*u);return Object.fromEntries(Object.keys(defaults).map(k=>[k,lerp(a.p[k],b.p[k],smooth)]));}
// Half-tick samples make a short continuous blade trail during the fast sweep;
// they contain only lightning, never duplicate solid swords. Shrink across the
// blade's width as the trail ages while retaining blade length and exact grip.
function withLightning(clip,t,phase){
 const sampled=sample(clip,t);
 if(clip.id===19&&phase===3&&t<12){const blend=t/12;for(const [n,v] of Object.entries(kneeling))sampled[n]=lerp(v,sampled[n],blend);}
 const o=posed(sampled,phase,clip.id),hit=hitTick.get(clip.id),isSweep=[3,4,6,11,17,20,21].includes(clip.id);
 const visible=phase!==3&&!([9,18,19,22,23,24].includes(clip.id));
 const active=visible&&(windIds.has(clip.id)||hit!==undefined||[20,21].includes(clip.id));
 const power=active?(hit!==undefined&&Math.abs(t-hit)<=1?1.45:1.05):.48;
 for(const[kind,weapon]of[['weapon','weapon'],['giant','giant_weapon']]){
  const w=o[weapon],fx=structuredClone(w);
  fx.s=visible?[w.s[0]*power,w.s[1],w.s[2]*power]:[0,0,0];o[kind+'_fx']=fx;
  for(let n=1;n<=3;n++){
   const prev=posed(sample(clip,Math.max(0,t-n*.55)),phase,clip.id)[weapon];
   const tail=structuredClone(prev),show=visible&&isSweep&&t>=1&&(hit===undefined||t<=hit+3);
   const taper=[.74,.52,.30][n-1];tail.s=show?[prev.s[0]*taper,prev.s[1],prev.s[2]*taper]:[0,0,0];
   o[kind+'_trail_'+n]=tail;
  }
 }
 // Concentrate energy between the fingers before contact, release a broken
 // lightning crown on the actual contact frame, then rapidly extinguish it.
 // Rear hands keep the smaller charged form so flashes cannot cover the face.
 const handCast=[7,8,12,13,14,15,16,17].includes(clip.id),variant=Math.floor(t/2)%2;
 const release=hit!==undefined&&t>=hit&&t<=hit+2;
 const handPower=hit===undefined?.7+.3*Math.min(t/6,1):t<hit?.85-.32*t/hit:t===hit?1.15:t===hit+1?.82:t===hit+2?.48:0;
 for(const[n,hand]of Object.entries(palmParts)){
  const v=structuredClone(o[hand]),rear=n.includes('rear'),allow=n==='palm_main_r'?[12,13,16,17].includes(clip.id):handCast;
  const on=phase===2&&allow&&visible&&handPower>0;
  v.s=on?v.s:[0,0,0];v.itemModel=palmModel(n,clip.id,hit!==undefined&&t<hit?'focus':release&&!rear,variant);o[n]=v;
 }
 const fore=o.left_forearm,skin={t:add(fore.t,rot(fore.q,[0,-.22*fore.s[1],0])),q:[...fore.q],s:Array(3).fill(0)};
 if(phase===0&&[7,8].includes(clip.id)&&handPower>0)skin.s=times(fore.s,.42);
 skin.itemModel=palmModel('palm_skin',clip.id,hit!==undefined&&t<hit?'focus':release,variant);o.palm_skin=skin;
 const chakra=structuredClone(o.chakra),chakraOn=phase===2&&visible&&(active||t%16<=2);
 chakra.s=chakraOn?times(chakra.s,hit!==undefined&&t===hit?1.10:1):[0,0,0];
 chakra.itemModel=`fx_weapon/chakra_${variant}`;o.chakra_fx=chakra;
 return o;
}
const poseLines=(o)=>pnames.map(n=>`data merge entity @e[tag=rlk_rd_${n},limit=1] {interpolation_duration:1,start_interpolation:0,transformation:${nbt(o[n])}${o[n].itemModel?`,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/${o[n].itemModel}"}}`:''}}`);
// The reference's final disappearance becomes six distinct translucent display
// splinters lifting away from the collapsing body. Nothing persists after cleanup.
for(let i=0;i<3;i++)model('death_shard_'+i,[box([7.2,3,7.6],[8.8,12,8.4],i===0?'deathViolet':'deathGlow'),box([7.65,2.3,7.4],[8.35,12.8,8.6],'deathWhite'),box([6.3,5.2,7.65],[7.2,8.4,8.35],'deathGlow'),box([8.8,7.8,7.7],[9.8,11.0,8.3],'deathViolet')]);
const deathParts=Array.from({length:6},(_,i)=>`rlk_rd_death_${i}`);
fn('death_fx_spawn',['kill @e[tag=rlk_rd_death_fx]',...deathParts.map((n,i)=>`summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_death_fx","${n}"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",brightness:{block:15,sky:15},interpolation_duration:1,teleport_duration:0,view_range:3f,width:0f,height:0f,shadow_radius:0f,transformation:{translation:[0f,0.8f,0f],left_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f],right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/death_shard_${i%3}"}}}`)]);
for(let t=0;t<=48;t++){
 const u=Math.max(0,Math.min(1,(t-18)/30)),envelope=Math.sin(u*Math.PI),lines=[];
 for(let i=0;i<6;i++){const a=i*Math.PI/3+.13,spread=.25+u*(1.0+(i%2)*.55),height=.55+u*(2.7+(i%3)*.4),scale=(.5+(i%2)*.25)*envelope,v={t:[Math.cos(a)*spread,height,Math.sin(a)*spread],q:q([12+u*60,a*180/Math.PI+u*80,20*Math.sin(i+u*3)]),s:[scale,scale*(1.3+u),scale]};lines.push(`data merge entity @e[tag=${deathParts[i]},limit=1] {interpolation_duration:1,start_interpolation:0,transformation:{translation:${arr(v.t)},left_rotation:${arr(v.q)},scale:${arr(v.s)},right_rotation:[0f,1f,0f,0f]}}`);}
 fn('death_fx/'+t,lines);
}
fn('death_fx_tick',Array.from({length:49},(_,t)=>`execute if score @s rdRigT matches ${t} run function rlk:boss/raiden/rig/death_fx/${t}`));
for(const c of clips){
 const dispatch=[];for(const phase of[0,1,2,3]){const phaseName=phase===0?'normal':phase===1?'forming':phase===2?'armored':'exhausted';for(let t=0;t<=c.length;t++){fn(`poses/${phaseName}/${c.name}/${t}`,poseLines(withLightning(c,t,phase)));dispatch.push(`execute if score @s rdPhase matches ${phase} if score @s rdRigT matches ${t} run function rlk:boss/raiden/rig/poses/${phaseName}/${c.name}/${t}`);}}
 fn('clip/'+c.name,[...(!c.loop?[`execute if score @s rdRigT matches ${c.length+1}.. run return 0`]:[`execute if score @s rdRigT matches ${c.length+1}.. run scoreboard players set @s rdRigT 0`]),...dispatch,...(c.id===19?['execute if score @s rdRigT matches 0 run function rlk:boss/raiden/rig/death_fx_spawn','function rlk:boss/raiden/rig/death_fx_tick']:[])]);
 fn('select/'+c.name,['# Only item identity changes here; the next pose interpolates from the current pose.',...['weapon','main_r_hand','main_l_hand',...fxNames,...powerFxNames].map(n=>`data modify entity @e[tag=rlk_rd_${n},limit=1] item.components."minecraft:item_model" set value "rlk:raiden/${modelFor(n,c.id)}"`)]);
 if([7,12,14,16].includes(c.id))for(const i of[0,1])fn(`charge_mesh/${c.id}_${i}`,powerFxNames.filter(n=>n.startsWith('palm_')).map(n=>`data modify entity @e[tag=rlk_rd_${n},limit=1] item.components."minecraft:item_model" set value "rlk:raiden/${palmModel(n,c.id,false,i)}"`));
}
fn('init',['# Private animation state. Safe to call on datapack reload.',...['rdRigA','rdRigT','rdRigP','rdRigHit'].map(o=>`scoreboard objectives add ${o} dummy`),'scoreboard players set #four rdRigT 4']);
fn('lightning_tick',[
 '# Two genuine jagged meshes flicker on the exact blade, including held windup poses.',
 'scoreboard players operation #rdFx rdRigT = @s rdRigT',
 'scoreboard players operation #rdFx rdRigT %= #four rdRigT',
 ...[0,1].flatMap(i=>[
  `execute if score #rdFx rdRigT matches ${i*2} unless score @s rdAnim matches 5..6 run data modify entity @e[tag=rlk_rd_weapon_fx,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/katana_${i}"`,
  `execute if score #rdFx rdRigT matches ${i*2} if score @s rdAnim matches 5..6 run data modify entity @e[tag=rlk_rd_weapon_fx,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/polearm_${i}"`,
  `execute if score #rdFx rdRigT matches ${i*2} run data modify entity @e[tag=rlk_rd_giant_fx,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/katana_${i}"`,
  `execute if score #rdFx rdRigT matches ${i*2} run data modify entity @e[tag=rlk_rd_chakra_fx,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/chakra_${i}"`,
  ...[7,12,14,16].map(anim=>`execute if score #rdFx rdRigT matches ${i*2} if score @s rdAnim matches ${anim} run function rlk:boss/raiden/rig/charge_mesh/${anim}_${i}`)
 ])
]);
fn('cleanup',['kill @e[tag=rlk_raiden_part]','kill @e[tag=rlk_rd_death_fx]']);
fn('flash',['# Called as the boss after a real body hit. Visual feedback only.','scoreboard players set @s rdRigHit 4','execute as @e[tag=rlk_raiden_part] run data merge entity @s {Glowing:1b,glow_color_override:13383423}']);
// A remote hand makes the targeted ground slam visibly reach its marked circle.
// Its entity origin is the captured ground point, never the moving boss/player.
// Advance it after boss AI each world tick, in the same order as hazard ages:
// summon tick = age 0; start the fast fall at age 25 and land at contact age 28.
// It deliberately does not carry rlk_raiden_part, so rig/tick cannot teleport it.
fn('target_slam_spawn',[
 '# Called positioned at the fixed target ground point. This helper does no damage.',
 'tag @e[tag=rlk_rd_slam_new] remove rlk_rd_slam_new',
 'summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_slam_hand","rlk_rd_slam_new"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:0,view_range:2.5f,width:16f,height:20f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,7f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/puppet_hand_open"}}}',
 'scoreboard players set @e[tag=rlk_rd_slam_new,limit=1] rdRigT -1',
 'tag @e[tag=rlk_rd_slam_new] remove rlk_rd_slam_new'
]);
fn('target_slam_tick',[
 '# @s = one floating hand, at its fixed ground origin. rdRigT is its age.',
 'execute unless entity @e[tag=rlk_raiden,scores={rdPhase=2,rdPat=13},limit=1] run return run kill @s',
 'scoreboard players add @s rdRigT 1',
 'execute if score @s rdRigT matches 1 run data merge entity @s {interpolation_duration:5,start_interpolation:0,transformation:{translation:[0f,7f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.5f,3.5f,3.5f],right_rotation:[0f,0f,0f,1f]}}',
 'execute if score @s rdRigT matches 21 run data merge entity @s {interpolation_duration:2,start_interpolation:0,transformation:{translation:[0f,7.35f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.5f,3.5f,3.5f],right_rotation:[0f,0f,0f,1f]}}',
 'execute if score @s rdRigT matches 25 run data merge entity @s {interpolation_duration:3,start_interpolation:0,transformation:{translation:[0f,1f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.5f,3.5f,3.5f],right_rotation:[0f,0f,0f,1f]}}',
 'execute if score @s rdRigT matches 31 run data merge entity @s {interpolation_duration:2,start_interpolation:0,transformation:{translation:[0f,1.4f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.5f,3.5f,3.5f],right_rotation:[0f,0f,0f,1f]}}',
 'execute if score @s rdRigT matches 35 run data merge entity @s {interpolation_duration:5,start_interpolation:0,transformation:{translation:[0f,1.8f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]}}',
 'execute if score @s rdRigT matches 41.. run kill @s'
]);
const initial=withLightning(clips[0],0,0);
fn('spawn',['function rlk:boss/raiden/rig/cleanup',...pnames.map(n=>`summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_part","rlk_raiden_aux","rlk_rd_${n}"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:2.5f,width:16f,height:16f,shadow_radius:0f,brightness:{block:${Object.hasOwn(bodySpecs,n)?12:15},sky:15},transformation:${nbt(initial[n])},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/${modelFor(n)}"}}}`),'scoreboard players set @s rdRigA -1','scoreboard players set @s rdRigP -1','scoreboard players set @s rdRigT 0','scoreboard players set @s rdRigHit 0','execute rotated as @s rotated ~ 0 run tp @e[tag=rlk_raiden_part] ~ ~ ~ ~ 0']);
fn('changed',['scoreboard players set @s rdRigT 0','scoreboard players operation @s rdRigA = @s rdAnim','scoreboard players operation @s rdRigP = @s rdPhase',...clips.map(c=>`execute if score @s rdAnim matches ${c.id} run function rlk:boss/raiden/rig/select/${c.name}`)]);
fn('tick',['# @s = unique real boss. Parts inherit body yaw but never pitch.','execute unless entity @e[tag=rlk_raiden_part,limit=1] run function rlk:boss/raiden/rig/spawn','execute rotated as @s rotated ~ 0 run tp @e[tag=rlk_raiden_part] ~ ~ ~ ~ 0','execute unless score @s rdAnim = @s rdRigA run function rlk:boss/raiden/rig/changed','execute unless score @s rdPhase = @s rdRigP run function rlk:boss/raiden/rig/changed',...clips.map(c=>`execute if score @s rdAnim matches ${c.id} run function rlk:boss/raiden/rig/clip/${c.name}`),'function rlk:boss/raiden/rig/lightning_tick','execute if score @s rdRigHit matches 1 run execute as @e[tag=rlk_raiden_part] run data merge entity @s {Glowing:0b}','execute if score @s rdRigHit matches 1.. run scoreboard players remove @s rdRigHit 1','scoreboard players add @s rdRigT 1']);
json(path.join(here,'raiden_rig_manifest.json'),{parts:pnames.length,phase:{0:'normal',1:'transforming',2:'Baleful Shadowlord',3:'exhausted'},armSilhouette:'two skin arms, giant right sword arm, giant left support palm, two smaller rear puppet arms',lightning:{weaponDisplays:8,palmDisplays:5,chakraDisplays:1,materials:'violet geometry and exposed white seams',hands:'exact hand pivot/rotation/scale; charge, inward focus, contact release; smaller rear hands never emit large release crowns',chakra:'sparse outer-rim forks; idle intermittent, charged attacks sustained; empty centre preserves face visibility'},clips:clips.map(({id,name,length,loop})=>({id,name,length,loop:!!loop})),integration:'Call rig/init from load, rig/spawn and rig/tick as the real boss at its feet. rdAnim selects a state; private rdRigT resets on rdAnim/rdPhase changes. rig/flash is optional body-hit feedback. rig/cleanup deletes all parts. Supplied skin remains byte-identical.'});
console.log(`Built Raiden: ${pnames.length} animated parts, ${clips.length} motion states, four phase forms, three encounter objects and one illusion.`);
