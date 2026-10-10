// Original dimensional arm and horizontal katana cut for the final calamity.
// Native display geometry; no sampled audio, particles, or borrowed animation.
// Call start at arena origin (0,201,0), tick as the boss reading rdTime, cleanup on cancel.
// Armour/blade colours are the shared opaque swatches of build_raiden_materials.py (build it first).
// node tools/build_raiden_judgment_rig.mjs --resourcepack <resourcepack>
//
// The cut, as the locked dome camera sees it (eye at arena (0,3,13) looking north: screen-left
// = -X/west, screen-right = +X/east): a lilac puppet arm reaches out of the rift, lifts the pale
// katana, draws it back to the LEFT and holds it level with its cutting edge turned toward the
// player; it then cuts horizontally LEFT -> RIGHT at dome height, edge leading, crosses the dome
// on contact tick 120, follows through to the right and withdraws into the rift by tick 152.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const arg=n=>{const i=process.argv.indexOf(n);return i<0?null:process.argv[i+1];};
const dp=path.resolve(arg('--datapack')||path.join(here,'..'));
const rp=path.resolve(arg('--resourcepack'));
const assets=path.join(rp,'assets/rlk');
const put=(p,s)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,s+'\n');};
const json=(p,o)=>put(p,JSON.stringify(o));
const fn=(n,a)=>put(path.join(dp,'data/rlk/function/boss/raiden/judgment_rig',n+'.mcfunction'),a.join('\n'));
const palette=['void','violet','lavender','white','cyan','shadow','violet_dense','glow','afterglow'];
const textures=Object.fromEntries(palette.map(n=>[n,'rlk:raiden/fx/'+n]));
// Opaque Shadowlord armour swatches, the same ones the armoured rig uses.
Object.assign(textures,Object.fromEntries(Object.entries({lilac:'arm_lilac',shade:'arm_shade',deep:'arm_deep',tomoe:'arm_tomoe',gdull:'gold_dull',bpale:'blade_pale',bedge:'blade_edge',bcore:'blade_core',grip:'grip_dark',nail:'nail_glow'}).map(([k,v])=>[k,'rlk:raiden/fx/'+v])));
const sides=['north','south','east','west','up','down'];
const box=(a,b,c,over={})=>({from:a,to:b,shade:false,faces:Object.fromEntries(sides.map(n=>[n,{texture:'#'+(over[n]||c),uv:[0,0,16,16]}]))});
// Armour and blade keep vanilla directional face shading so the plates read as volumes.
const solid=(a,b,c,over={})=>({from:a,to:b,faces:Object.fromEntries(sides.map(n=>[n,{texture:'#'+(over[n]||c),uv:[0,0,16,16]}]))});
const centered=(p,s,c)=>box(p.map((x,i)=>8+x-s[i]/2),p.map((x,i)=>8+x+s[i]/2),c);
const model=(name,e)=>{for(const el of e)for(const v of[...el.from,...el.to])if(v<-16||v>32)throw new Error(name+': element outside the -16..32 model cube');json(path.join(assets,'models/item/raiden/judgment',name+'.json'),{ambientocclusion:false,textures:{...textures,particle:textures.violet},elements:e});json(path.join(assets,'items/raiden/judgment',name+'.json'),{model:{type:'minecraft:model',model:'rlk:item/raiden/judgment/'+name}});};
const line=(points,w,c,step=.35)=>{const e=[];for(let n=1;n<points.length;n++){const a=points[n-1],b=points[n],k=Math.max(1,Math.ceil(Math.hypot(...b.map((v,i)=>v-a[i]))/step));for(let i=0;i<k;i++){const p=a.map((v,j)=>v+(b[j]-v)*i/k),q=a.map((v,j)=>v+(b[j]-v)*(i+1)/k);e.push(centered(p.map((v,j)=>(v+q[j])/2),p.map((v,j)=>Math.abs(q[j]-v)+w),c));}}return e;};
const eyePoint=(a,rx=20,ry=8,z=0)=>[rx*Math.cos(a),ry*Math.sin(a)*Math.pow(Math.abs(Math.sin(a)),.22),z];
function eyeFill(color,rx=20,ry=8){const e=[];for(let j=-32;j<32;j++){const y=(j+.5)*ry/32,x=rx*Math.pow(Math.max(0,1-Math.pow(Math.abs(y)/ry,1.65)),.72);e.push(centered([0,y,0],[x*2,ry/32+.015,.025],color));}return e;}
model('rift_void',eyeFill('shadow'));
model('rift_depth',eyeFill('void',18.5,7.1));
model('rift_haze',eyeFill('lavender',20.9,8.45));
function eyeRim(variant,glow=false){const e=[];for(let i=0;i<72;i++){const a=i*Math.PI*2/72,b=(i+1)*Math.PI*2/72,m=(a+b)/2,zig=(i%5===variant?.8:0);e.push(...line([eyePoint(a,20,8,.1),eyePoint(m,20+zig,8+zig*.35,.1),eyePoint(b,20,8,.1)],glow?.68:.16,glow?'violet':'white',.5));}if(!glow)for(let i=0;i<12;i++){const a=i*Math.PI/6+.07*variant,p=eyePoint(a,20,8,.15),q=eyePoint(a+.025,21.1,9,.15),r=eyePoint(a-.025,22.4,9.3,.15);e.push(...line([p,q,r],.18,'cyan'));}return e;}
for(let i=0;i<2;i++)model('rift_edge_'+i,eyeRim(i));
model('rift_edge_glow',eyeRim(0,true));
let seed=7919;const rand=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
const stars=[];for(let i=0;i<58;i++){const a=rand()*Math.PI*2,r=Math.sqrt(rand())*.87,x=Math.cos(a)*18*r,y=Math.sin(a)*6.5*r,z=.35+rand()*.35,s=.065+rand()*.13;stars.push(centered([x,y,z],[s*3,s,s/2],i%3?'lavender':'white'));stars.push(centered([x,y,z+.008],[s,s*3,s/2],i%4?'violet_dense':'cyan'));}model('rift_stars',stars);
const iris=[];for(let petal=0;petal<3;petal++){const a=petal*Math.PI*2/3;for(let i=0;i<18;i++){const t=i/17,b=a+t*1.8,r=2.6+2.3*t;iris.push(...line([[Math.cos(b)*r,Math.sin(b)*r*.64,.4],[Math.cos(b+.09)*(r+.1),Math.sin(b+.09)*(r+.1)*.64,.4]],.19,'violet_dense'));}}model('rift_iris',iris);
const fragments=[];for(let i=0;i<14;i++){const a=i*Math.PI*2/14,r=12+rand()*5;fragments.push(centered([Math.cos(a)*r,Math.sin(a)*5,.5+rand()],[.5+rand()*.8,1.0+rand()*1.2,.13],i%3===0?'white':'violet_dense'));}model('rift_fragments',fragments);

// ---- Puppet arm: arm_lilac plates, arm_shade sides, arm_deep joints, gold_dull trims ----------
// Bones have their proximal pivot at [8,8,8] and extend along local -Y (upper 20 px, forearm
// 22 px, so one uniform scale keeps the tomoe discs round). Local -Z is the outer face; the
// poser turns it toward the player camera, so it carries the large tomoe disc. The upper arm's
// dark root sleeve reaches back up through the rift plane from the shoulder pivot.
const plate={east:'shade',west:'shade',south:'shade'};
function face(dir,c,[u0,u1],[v0,v1],[d0,d1],tex){const at={'-z':(u,v,d)=>[c[0]+u,c[1]+v,c[2]-d],'+z':(u,v,d)=>[c[0]-u,c[1]+v,c[2]+d],'-x':(u,v,d)=>[c[0]-d,c[1]+v,c[2]-u],'+x':(u,v,d)=>[c[0]+d,c[1]+v,c[2]+u]}[dir];const a=at(u0,v0,d0),b=at(u1,v1,d1);return solid(a.map((x,i)=>Math.min(x,b[i])),a.map((x,i)=>Math.max(x,b[i])),tex);}
// Tomoe disc on one face: dull-gold rim, arm_tomoe field and three swirling gold commas.
function tomoe(dir,c,r){const disc=(R,d,tex)=>[[R,.42*R],[.42*R,R],[.72*R,.72*R]].map(([a,b])=>face(dir,c,[-a,a],[-b,b],d,tex));const e=[...disc(r,[-.1,.16],'gdull'),...disc(.78*r,[-.1,.28],'tomoe')];
 for(let i=0;i<3;i++){const a=Math.PI/2+i*2*Math.PI/3;for(let k=0;k<3;k++){const b=a+.5*k,s=r*[.19,.12,.065][k],u=Math.cos(b)*(.33+.09*k)*r,v=Math.sin(b)*(.33+.09*k)*r;e.push(face(dir,c,[u-s,u+s],[v-s,v+s],[0,.4],'gdull'));}}return e;}
model('upper_arm',[
 solid([5.9,10.5,5.9],[10.1,17.5,10.1],'deep',{up:'tomoe'}),solid([5.2,5.0,5.2],[10.8,11.0,10.8],'deep'),solid([4.5,5.8,6.0],[11.5,10.2,10.0],'deep'),solid([6.0,5.8,4.5],[10.0,10.2,11.5],'deep'),
 solid([5.6,-12,5.6],[10.4,6,10.4],'deep'),
 solid([4.4,-8.8,4.4],[11.6,4.0,11.6],'lilac',plate),
 solid([4.15,3.3,4.15],[11.85,4.4,11.85],'gdull'),solid([4.15,-9.2,4.15],[11.85,-8.1,11.85],'gdull'),solid([4.25,-2.95,4.25],[11.75,-2.35,11.75],'deep'),
 ...tomoe('-z',[8,.55,4.4],2.55),...tomoe('+z',[8,-5.6,11.6],1.8),
 solid([5.0,-12,5.0],[11.0,-9.4,11.0],'shade',{up:'deep',down:'deep'})]);
model('forearm',[
 solid([4.8,4.6,5.4],[11.2,11.4,10.6],'deep'),solid([5.4,4.6,4.8],[10.6,11.4,11.2],'deep'),solid([4.5,7.3,4.5],[11.5,8.7,11.5],'gdull'),
 solid([5.7,-14,5.7],[10.3,6,10.3],'deep'),
 solid([4.3,-3.2,4.3],[11.7,4.6,11.7],'lilac',plate),solid([4.7,-10.9,4.7],[11.3,-2.7,11.3],'lilac',plate),
 solid([4.1,4.0,4.1],[11.9,5.0,11.9],'gdull'),solid([4.5,-11.3,4.5],[11.5,-10.4,11.5],'gdull'),solid([4.2,-3.3,4.2],[11.8,-2.6,11.8],'deep'),
 ...tomoe('-z',[8,.75,4.3],2.4),...tomoe('-z',[8,-6.9,4.7],1.55),
 solid([5.1,-14,5.1],[10.9,-11.1,10.9],'shade',{up:'deep',down:'deep'})]);
// Closed right fist. Pivot [8,8,8] is the wrist (the forearm arrives from local +X); the hand runs
// toward -X, its back (tomoe) faces -Z and the fingers curl round the sword grip, whose axis
// runs along local Y through GRIP. The thumb lies over the grip at +Y, under the tsuba.
const GRIP=[2.2,11.2];
const fist=[
 solid([5.4,5.4,5.8],[10.6,10.6,10.2],'deep'),solid([5.8,5.0,5.4],[10.2,11.0,10.6],'deep'),solid([7.2,4.7,5.0],[8.6,11.3,11.0],'gdull'),
 solid([1.6,4.0,5.2],[7.6,12.0,9.0],'lilac',{south:'shade',east:'shade',up:'shade',down:'shade'}),
 solid([3.9,4.3,8.9],[7.3,11.7,10.5],'shade'),solid([.9,3.8,5.0],[2.1,12.2,9.2],'gdull'),
 ...tomoe('-z',[4.6,8,5.2],2.2)];
for(let i=0;i<4;i++){const y0=4.15+i*1.95,y1=y0+1.75,s=i===3?.3:0;
 fist.push(solid([-1.3+s,y0,5.6],[1.2,y1,9.4],'lilac',{west:'shade',up:'shade',down:'shade'}),solid([-1.6+s,y0+.1,9.0],[.4,y1-.1,13.0],'lilac',{west:'shade',up:'shade',down:'shade'}),
  solid([.2,y0+.15,12.95],[3.0,y1-.15,14.4],'lilac',{up:'shade',down:'shade',south:'shade'}),solid([-1.45+s,y0+.05,8.75],[.6,y1-.05,9.6],'deep'),solid([.05,y0+.2,12.6],[.6,y1-.2,14.2],'deep'),
  solid([2.85,y0+.3,13.1],[3.45,y1-.3,14.1],'nail'));}
fist.push(solid([3.75,11.9,8.8],[6.6,13.6,12.0],'lilac',{up:'shade',down:'shade'}),solid([1.6,12.0,12.7],[4.6,13.5,14.3],'lilac',{up:'shade'}),solid([1.3,12.1,13.4],[2.1,13.4,14.4],'nail'),solid([3.75,11.85,11.4],[4.7,13.65,12.2],'deep'));
model('closed_hand',fist);
// Electro seams: violet light leaking from the joint gaps and cyan sparks on the side plates.
function seams(len,r){const e=[];for(const y of[0,-len])e.push(centered([0,y,0],[r*2+1.0,1.1,r*2+1.0],'violet'),centered([0,y,0],[r*2+2.0,.5,r*2+2.0],'glow'));
 for(const s of[-1,1])e.push(...line([[s*(r+.15),-.18*len,.6*s],[s*(r+.35),-.36*len,-.5*s],[s*(r+.15),-.55*len,.4*s],[s*(r+.4),-.78*len,-.3*s]],.2,'cyan'));return e;}
model('upper_veins',seams(20,3.7));model('forearm_veins',seams(22,3.6));

// ---- Katana -------------------------------------------------------------------------------
// Blade along local +Y; display pivot [8,8,8] sits on the grip inside the fist.
// EDGE SIDE: local -X is the cutting edge (the convex side of the curve, a continuous blade_edge
// strip); local +X is the spine (blade_core); the flats face +-Z. The poser sets local -X to the
// direction the blade travels in the cut, so the edge leads.
const BLADE={y0:13,y1:31.6,n:24};
const bladeAt=i=>{const t=i/(BLADE.n-1),h=(BLADE.y1-BLADE.y0)/BLADE.n,y=BLADE.y0+h*i,c=8.15+1.35*t*t,base=2.5-.55*t,w=[1.55,.95,.42][i-(BLADE.n-3)]??base,xr=c+base/2;return{y,h,xl:xr-w,xr,w};};
const katana=[solid([6.85,.6,6.85],[9.15,1.7,9.15],'gdull'),
 solid([7.25,1.6,7.45],[8.75,11.05,8.55],'grip'),solid([7.45,1.6,7.25],[8.55,11.05,8.75],'grip'),
 solid([5.3,11.0,6.5],[10.7,11.7,9.5],'gdull'),solid([6.5,11.0,5.3],[9.5,11.7,10.7],'gdull'),solid([5.75,11.0,5.75],[10.25,11.7,10.25],'gdull'),
 solid([6.2,10.94,6.9],[9.8,11.76,9.1],'deep'),solid([6.9,10.94,6.2],[9.1,11.76,9.8],'deep'),
 solid([6.95,11.7,7.3],[9.45,13.05,8.7],'gdull')];
for(let y=2.3;y<10.4;y+=1.35)katana.push(solid([7.12,y,7.12],[8.88,y+.42,8.88],'gdull'),solid([7.6,y+.42,7.08],[8.4,y+.9,8.92],'deep'));
for(let i=0;i<BLADE.n;i++){const{y,h,xl,xr,w}=bladeAt(i),top=y+h+.02,edge=Math.min(.62,w*.55);
 katana.push(solid([xl-.12,y,7.68],[xl+edge,top,8.32],'bedge'),solid([xl+edge-.1,y,7.5],[xr,top,8.5],'bpale',{east:'bcore'}));
 if(i<BLADE.n-3)katana.push(solid([xr-1.0,y,7.42],[xr-.45,top,8.58],'bcore'));}
model('katana',katana);
// Glows follow the curved blade; the aura leans out past the cutting edge.
function bladeGlow(color,extra,thick,lean=0){const e=[];for(let i=0;i<BLADE.n;i++){const{y,h,xl,xr}=bladeAt(i);e.push(centered([(xl+xr)/2-8-lean*extra,y+h/2-8,0],[xr-xl+extra,h+.06,thick],color));}return e;}
model('blade_aura',bladeGlow('violet',1.4,.42,.32));
model('blade_haze',bladeGlow('glow',3.6,.26,.22));
model('blade_trail_near',bladeGlow('violet',1,.5));
model('blade_trail_far',bladeGlow('afterglow',.7,.4));
model('blade_trail_faint',bladeGlow('lavender',.3,.3));
for(let v=0;v<2;v++){const e=[];for(const s of[-1,1]){const pts=[];for(let i=0;i<11;i++){const b=bladeAt(Math.min(BLADE.n-1,Math.round(i*2.2)));pts.push([(s<0?b.xl:b.xr)-8+s*(.5+((i+v)%3===0?.85:.15)),b.y+b.h/2-8,s*.55]);}e.push(...line(pts,.21,'violet_dense'));e.push(...line(pts.map(p=>[p[0],p[1],p[2]+s*.17]),.07,'white'));for(const n of[2,6]){const p=pts[n];e.push(...line([p,[p[0]+s*1.3,p[1]+1.1,p[2]],[p[0]+s*.85,p[1]+2.2,p[2]],[p[0]+s*1.9,p[1]+3.2,p[2]]],.12,'cyan'));}}model('blade_lightning_'+v,e);}

// Quaternion helpers. Model coordinates are world-aligned; the final right-Y-pi
// correction cancels Minecraft's additional item-display model rotation.
const rad=x=>x*Math.PI/180;
const mul=(a,b)=>{const[x,y,z,w]=a,[X,Y,Z,W]=b;return[w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W,w*W-x*X-y*Y-z*Z];};
const q=e=>{const[x,y,z]=e.map(v=>rad(v)/2);return mul(mul([0,0,Math.sin(z),Math.cos(z)],[0,Math.sin(y),0,Math.cos(y)]),[Math.sin(x),0,0,Math.cos(x)]);};
const rot=(a,v)=>mul(mul(a,[...v,0]),[-a[0],-a[1],-a[2],a[3]]).slice(0,3);
const add=(a,b)=>a.map((v,i)=>v+b[i]),sub=(a,b)=>a.map((v,i)=>v-b[i]),times=(a,s)=>a.map(v=>v*s),lerp=(a,b,t)=>a.map((v,i)=>v+(b[i]-v)*t),dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0),norm=a=>times(a,1/Math.max(.00001,Math.hypot(...a))),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const clamp=x=>Math.max(0,Math.min(1,x)),smooth=x=>{x=clamp(x);return x*x*(3-2*x);};
function basisQuat(x,y,z){const m=[x[0],y[0],z[0],x[1],y[1],z[1],x[2],y[2],z[2]],tr=m[0]+m[4]+m[8];let a;if(tr>0){const s=Math.sqrt(tr+1)*2;a=[(m[7]-m[5])/s,(m[2]-m[6])/s,(m[3]-m[1])/s,s/4];}else if(m[0]>m[4]&&m[0]>m[8]){const s=Math.sqrt(1+m[0]-m[4]-m[8])*2;a=[s/4,(m[1]+m[3])/s,(m[2]+m[6])/s,(m[7]-m[5])/s];}else if(m[4]>m[8]){const s=Math.sqrt(1+m[4]-m[0]-m[8])*2;a=[(m[1]+m[3])/s,s/4,(m[5]+m[7])/s,(m[2]-m[6])/s];}else{const s=Math.sqrt(1+m[8]-m[0]-m[4])*2;a=[(m[2]+m[6])/s,(m[5]+m[7])/s,s/4,(m[3]-m[1])/s];}return norm(a);}

// ---- Motion ---------------------------------------------------------------------------------
// Arena-relative world coordinates. The shoulder sits half a block below the rift plane (the root
// sleeve reaches up into it); CAM is the locked dome camera eye (camera/hold: 0,204,13 yaw 180).
const SHOULDER=[0,8.75,-6.45],CAM=[0,3,13];
const ARM=3.8,L1=20/16*ARM,L2=22/16*ARM,HAND=4.4,SWORD=8.4;
const GRIP_OFF=[(GRIP[0]-8)/16,0,(GRIP[1]-8)/16];
// Keys: h = grip point; a = [heading, elevation] of the blade in degrees. Heading 0 points at the
// player (+Z), -90 to screen-left (-X), +90 to screen-right (+X). hold = zero velocity at the key;
// v = explicit per-tick velocities (the cut is fastest at contact and eases in/out around it).
const keys=[
 {t:54,h:SHOULDER,a:[-80,80],hold:1},
 {t:76,h:[-3.4,6.9,-4.8],a:[-90,70]},
 {t:94,h:[-6.2,5.6,-3.8],a:[-96,38]},
 {t:108,h:[-7.0,4.4,-3.3],a:[-100,15]},
 {t:116,h:[-7.5,4.2,-3.5],a:[-106,11],hold:1},
 {t:120,h:[0,2.5,-3.9],a:[0,-2],v:{h:[3.6,0,-.1],a:[58,0]}},
 {t:125,h:[6.8,3.2,-4.7],a:[104,4],hold:1},
 {t:133,h:[5.8,5.8,-5.3],a:[112,50]},
 {t:140,h:[3.4,7.3,-5.9],a:[100,76]},
 {t:152,h:SHOULDER,a:[95,85],hold:1}
];
function channel(name,t){const n=keys.length;if(t<=keys[0].t)return keys[0][name];if(t>=keys[n-1].t)return keys[n-1][name];
 let i=0;while(keys[i+1].t<=t)i++;const A=keys[i],B=keys[i+1],T=B.t-A.t,u=(t-A.t)/T;
 const tan=k=>{const K=keys[k];if(K.v&&K.v[name])return K.v[name];if(K.hold||k===0||k===n-1)return K[name].map(()=>0);return sub(keys[k+1][name],keys[k-1][name]).map(v=>v/(keys[k+1].t-keys[k-1].t));};
 const h00=2*u*u*u-3*u*u+1,h10=u*u*u-2*u*u+u,h01=-2*u*u*u+3*u*u,h11=u*u*u-u*u,m0=tan(i),m1=tan(i+1);
 return A[name].map((v,j)=>h00*v+h10*T*m0[j]+h01*B[name][j]+h11*T*m1[j]);}
// Two-bone arm with fixed segment lengths. The elbow bends toward a fixed pole on the player's left
// (it trails the left-to-right cut and never flips) and stays in front of the rift plane.
function ik(s,w,a,b,pole){const v=sub(w,s),n=norm(v),D=Math.min(Math.max(Math.hypot(...v),Math.abs(a-b)+1e-4),(a+b)*.9995),x=(a*a-b*b+D*D)/(2*D),y=Math.sqrt(Math.max(0,a*a-x*x));let p=sub(pole,times(n,dot(pole,n)));if(Math.hypot(...p)<1e-3)p=cross(n,[1,0,0]);p=norm(p);return{elbow:add(s,add(times(n,x),times(p,y))),wrist:add(s,times(n,D)),short:Math.hypot(...v)-D};}
// Bone frame: local -Y runs from a to b, local -Z turns toward the camera (tomoe outward).
function boneQ(a,b){const y=norm(sub(a,b));let f=sub(CAM,lerp(a,b,.5));f=sub(f,times(y,dot(f,y)));if(Math.hypot(...f)<.5)f=sub([0,1,0],times(y,y[1]));const z=times(norm(f),-1);return basisQuat(cross(y,z),y,z);}
let worstReach=0;
function rigAt(t){
 const size=smooth((t-54)/20)*(1-smooth((t-139)/13)),tense=smooth((t-104)/8)*(1-smooth(t-115));
 // A short tense tremble while the blade is held back before the cut.
 const h=add(channel('h',t),times([Math.sin(t*2.9),Math.sin(t*4.1+1),Math.sin(t*3.3+2)],.07*tense)),[heading,elev]=add(channel('a',t),[Math.sin(t*3.7)*1.2*tense,0]);
 const ph=rad(heading),be=rad(elev),d=[Math.sin(ph)*Math.cos(be),Math.sin(be),Math.cos(ph)*Math.cos(be)],edge=[Math.cos(ph),0,-Math.sin(ph)];
 // Blade frame: local +Y = blade, local -X = edge = horizontal tangent of the sweep (left -> right).
 const swordQ=basisQuat(times(edge,-1),d,cross(d,edge));
 if(size<.0001)return{size:0,upper:[SHOULDER,[0,0,0,1]],forearm:[SHOULDER,[0,0,0,1]],hand:[SHOULDER,[0,0,0,1]],sword:[SHOULDER,swordQ]};
 const pole=norm([-1,0,.45]),handFrame=sol=>{let F=norm(sub(sol.wrist,sol.elbow));F=norm(add(sub(F,times(d,dot(F,d))),times(edge,.5)));const X=times(F,-1);return basisQuat(X,d,cross(X,d));};
 // The fist hangs from the wrist; its local -X follows the forearm (biased toward the edge, so the
 // wrist always sits on the spine side and the frame never flips). Solve the wrist so that the
 // grip lands on the keyed point.
 let wrist=add(h,[0,size,0]),sol,handQ;
 for(let it=0;it<6;it++){sol=ik(SHOULDER,wrist,L1*size,L2*size,pole);handQ=handFrame(sol);wrist=sub(h,rot(handQ,times(GRIP_OFF,HAND*size)));}
 sol=ik(SHOULDER,wrist,L1*size,L2*size,pole);handQ=handFrame(sol);worstReach=Math.max(worstReach,sol.short);
 const grip=add(sol.wrist,rot(handQ,times(GRIP_OFF,HAND*size)));
 return{size,upper:[SHOULDER,boneQ(SHOULDER,sol.elbow)],forearm:[sol.elbow,boneQ(sol.elbow,sol.wrist)],hand:[sol.wrist,handQ],sword:[grip,swordQ],d,edge};
}
const parts={rift_void:'rift_void',rift_depth:'rift_depth',rift_haze:'rift_haze',rift_edge:'rift_edge_0',rift_edge_glow:'rift_edge_glow',rift_stars:'rift_stars',rift_iris:'rift_iris',rift_fragments:'rift_fragments',upper:'upper_arm',forearm:'forearm',hand:'closed_hand',upper_veins:'upper_veins',forearm_veins:'forearm_veins',sword:'katana',blade_aura:'blade_aura',blade_haze:'blade_haze',blade_lightning:'blade_lightning_0',trail1:'blade_trail_near',trail2:'blade_trail_far',trail3:'blade_trail_faint'};
const scaled=([t,q],s)=>({t,q,s:[s,s,s]});
function sword(t){const r=rigAt(t);return scaled(r.sword,SWORD*r.size);}
function pose(t){
 const opening=smooth((t-24)/22),openHeight=.035+.965*smooth((t-38)/27),closing=1-smooth((t-140)/14),pulse=1+.025*Math.sin(t*.34),portal=[0,9.15,-6.8],portalQ=q([70,0,0]),o={};
 const portalScale=[5.5*opening*closing,5.5*openHeight*closing,5.5*closing];
 for(const n of ['rift_void','rift_depth','rift_haze','rift_edge','rift_edge_glow','rift_stars','rift_iris','rift_fragments'])o[n]={t:[...portal],q:[...portalQ],s:[...portalScale]};
 o.rift_depth.t=add(portal,rot(portalQ,[0,0,-.03]));
 o.rift_haze.t=add(portal,rot(portalQ,[0,0,-.06]));o.rift_haze.s=times(portalScale,1.10*pulse);
 o.rift_edge_glow.s=times(portalScale,1.025*pulse);
 o.rift_stars.q=mul(portalQ,q([0,0,Math.sin(t*.018)*5]));o.rift_iris.q=mul(portalQ,q([0,0,t*.5]));
 o.rift_fragments.q=mul(portalQ,q([0,0,Math.sin(t*.11)*3]));o.rift_fragments.s=times(portalScale,1.0+.065*Math.sin(t*.085));
 o.rift_edge.model='rift_edge_'+(Math.floor(t/3)%2);
 const r=rigAt(t);
 o.upper=scaled(r.upper,ARM*r.size);o.forearm=scaled(r.forearm,ARM*r.size);o.hand=scaled(r.hand,HAND*r.size);
 o.upper_veins=structuredClone(o.upper);o.forearm_veins=structuredClone(o.forearm);
 o.sword=scaled(r.sword,SWORD*r.size);
 for(const n of['blade_aura','blade_haze','blade_lightning'])o[n]=structuredClone(o.sword);
 o.blade_lightning.model='blade_lightning_'+(Math.floor(t/2)%2);
 // Afterimages of the last two ticks of the cut, only while the blade is fast.
 for(let i=1;i<=3;i++){o['trail'+i]=sword(t-i*.65);if(t<117||t>127)o['trail'+i].s=[0,0,0];}
 return o;
}
const f=v=>(Math.abs(v)<.0000005?0:v).toFixed(6)+'f',arr=a=>'['+a.map(f).join(',')+']';
const nbt=v=>`{translation:${arr(v.t)},left_rotation:${arr(v.q)},scale:${arr(v.s)},right_rotation:[0f,1f,0f,0f]}`;
const tags=n=>`@e[tag=rlk_rd_j_${n},limit=1]`;
const previous={};
for(let t=0;t<=176;t++){
 // One-tick interpolation arrives at impact on rdTime=120, not a tick late.
 const p=pose(t+1),lines=[];
 for(const n of Object.keys(parts)){if(previous[n]&&dot(p[n].q,previous[n])<0)p[n].q=times(p[n].q,-1);previous[n]=[...p[n].q];lines.push(`data merge entity ${tags(n)} {interpolation_duration:1,start_interpolation:0,transformation:${nbt(p[n])}${p[n].model?`,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/judgment/${p[n].model}"}}`:''}}`);}
 fn('frame/'+t,lines);
}
fn('cleanup',['kill @e[tag=rlk_rd_judgment_rig]']);
const initial=pose(0);
fn('start',['# Fixed arena origin, independent of the hidden boss and camera.','function rlk:boss/raiden/judgment_rig/cleanup',...Object.entries(parts).map(([n,asset])=>`summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_judgment_rig","rlk_rd_j_${n}"],NoGravity:1b,Invulnerable:1b,Rotation:[0f,0f],billboard:"fixed",item_display:"none",brightness:{block:15,sky:15},view_range:4f,shadow_radius:0f,width:0f,height:0f,teleport_duration:0,interpolation_duration:1,transformation:${nbt(initial[n])},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/judgment/${asset}"}}}`)]);
fn('tick',['# Call as the unique boss. The arm is world-anchored and has no own hitbox.','execute unless score @s rdPhase matches 2 run return run function rlk:boss/raiden/judgment_rig/cleanup','execute unless score @s rdPat matches 15 run return run function rlk:boss/raiden/judgment_rig/cleanup',...Array.from({length:177},(_,t)=>`execute if score @s rdTime matches ${t} run function rlk:boss/raiden/judgment_rig/frame/${t}`),'execute if score @s rdTime matches 177.. run function rlk:boss/raiden/judgment_rig/cleanup']);
const hit=rigAt(120),tip=add(hit.sword[0],times(hit.d,(BLADE.y1-8)/16*SWORD));
console.log(`Built final calamity: ${Object.keys(parts).length} displays, 177 poses; left-to-right edge-first cut crosses the dome at tick120 (grip ${hit.sword[0].map(v=>v.toFixed(2))}, tip ${tip.map(v=>v.toFixed(2))}, edge ${hit.edge.map(v=>v.toFixed(2))}); arm reach shortfall ${worstReach.toFixed(3)}.`);
