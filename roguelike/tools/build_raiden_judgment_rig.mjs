// 만겁 (Raiden pattern 15): the rift that tears the sky open and the giant armoured arm that draws a katana out of it and
// cuts across the arena (the release's final-calamity rig, d765bab, restored on the user's request 10-22; reference video
// S:rd/src/user_refs/mangeop_ref.mp4). Native display geometry; vanilla sounds are played by the pattern (tenma.py p15).
//
// node tools/build_raiden_judgment_rig.mjs --resourcepack <unpacked pack> [--datapack <pack>] [--debug-dp <scratch dir>]
//   --debug-dp: copies judgment_rig/ there and writes rd_dbg/mg/<t> (the exact pose of every tick, no interpolation)
//
// Writes RP assets/rlk/{models/item,items}/raiden/judgment/*.json (22 models; textures: the rlk:raiden/fx/* palette and
// armour swatches of build_raiden_materials.py, the rlk:raiden/fxg/* strips of build_raiden_fx_textures.py: build both
// first) and DP data/rlk/function/boss/raiden/judgment_rig/{start,tick,clash,cleanup,frame/<t>} (rebuilt from scratch).
//
// Runtime (tenma.py p15): judgment_rig/start at the arena centre, facing the player (rlk_body) at rdTime T0; then
// judgment_rig/tick as the boss every tick up to T_END (key frames, each interpolated to the next key; cleanup at T_END).
// The parts carry rlk_rd_tmp / rlk_rd_tm, so the pattern's finish, pause, transformation and death remove them. They
// stand on one yaw toward the player, so the cut happens in front of whoever watches the flower, with the camera free.
// The rig frame: +Z toward the player, -X screen-left (as the player sees it), floor y = 0, the safe dome is the sphere
// r 8 about the origin. Rift opens T0.., the arm emerges 84.., draws back to the left and holds 146, cuts left -> right
// and strikes the dome edge-first on HIT (the lethal slash; the dome stops the blade), is thrown back when the dome
// cracks (160), withdraws by 186 and the rift collapses with the dome's shatter (176 -> 188). Nothing goes below the
// floor (hidden = scale 0 at the shoulder, never a teleport) and no solid part enters the dome (both checked here).
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const arg=n=>{const i=process.argv.indexOf(n);return i<0?null:process.argv[i+1];};
const dp=path.resolve(arg('--datapack')||path.join(here,'..'));
if(!arg('--resourcepack'))throw new Error('--resourcepack <unpacked pack> is required');
const rp=path.resolve(arg('--resourcepack'));
const assets=path.join(rp,'assets/rlk');
const put=(p,s)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,s+'\n');};
const json=(p,o)=>put(p,JSON.stringify(o));
const FN_DIR=path.join(dp,'data/rlk/function/boss/raiden/judgment_rig');
for(const d of[FN_DIR,path.join(assets,'models/item/raiden/judgment'),path.join(assets,'items/raiden/judgment')])fs.rmSync(d,{recursive:true,force:true});
const fn=(n,a)=>put(path.join(FN_DIR,n+'.mcfunction'),a.join('\n'));
const MODELS={};
const palette=['void','violet','lavender','white','cyan','shadow','violet_dense','glow','afterglow'];
const textures=Object.fromEntries(palette.map(n=>[n,'rlk:raiden/fx/'+n]));
// Opaque Shadowlord armour swatches, the same ones the armoured rig uses.
Object.assign(textures,Object.fromEntries(Object.entries({lilac:'arm_lilac',shade:'arm_shade',deep:'arm_deep',tomoe:'arm_tomoe',gdull:'gold_dull',bpale:'blade_pale',bedge:'blade_edge',bcore:'blade_core',grip:'grip_dark',nail:'nail_glow'}).map(([k,v])=>[k,'rlk:raiden/fx/'+v])));
const sides=['north','south','east','west','up','down'];
const box=(a,b,c,over={})=>({from:a,to:b,shade:false,faces:Object.fromEntries(sides.map(n=>[n,{texture:'#'+(over[n]||c),uv:[0,0,16,16]}]))});
// Armour and blade keep vanilla directional face shading so the plates read as volumes.
const solid=(a,b,c,over={})=>({from:a,to:b,faces:Object.fromEntries(sides.map(n=>[n,{texture:'#'+(over[n]||c),uv:[0,0,16,16]}]))});
const centered=(p,s,c)=>box(p.map((x,i)=>8+x-s[i]/2),p.map((x,i)=>8+x+s[i]/2),c);
const model=(name,e)=>{MODELS[name]=e;for(const el of e)for(const v of[...el.from,...el.to])if(v<-16||v>32)throw new Error(name+': element outside the -16..32 model cube');json(path.join(assets,'models/item/raiden/judgment',name+'.json'),{ambientocclusion:false,textures:{...textures,particle:textures.violet},elements:e});json(path.join(assets,'items/raiden/judgment',name+'.json'),{model:{type:'minecraft:model',model:'rlk:item/raiden/judgment/'+name}});};
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
// Glows, trails and lightning follow the blade as painted gradient cards (rlk:raiden/fxg/*,
// tools/build_raiden_fx_textures.py): flat cards in the blade plane (normal Z) and across it
// (normal X), u along the blade (hilt -> tip), two halves per card so they follow the curve.
// The aura leans out past the cutting edge (-X).
const fxCat=JSON.parse(fs.readFileSync(path.join(here,'raiden_fx_textures.json'),'utf8'));
const fxTex=Object.fromEntries(fxCat.textures.map(t=>[t.name,t.texture]));
const FPAIR={x:['east','west'],y:['up','down'],z:['south','north']};
const fCorners=(face,[x0,y0,z0],[x1,y1,z1])=>({north:[[x1,y1,z0],[x0,y1,z0],[x0,y0,z0],[x1,y0,z0]],south:[[x0,y1,z1],[x1,y1,z1],[x1,y0,z1],[x0,y0,z1]],east:[[x1,y1,z1],[x1,y1,z0],[x1,y0,z0],[x1,y0,z1]],west:[[x0,y1,z0],[x0,y1,z1],[x0,y0,z1],[x0,y0,z0]],up:[[x0,y1,z0],[x1,y1,z0],[x1,y1,z1],[x0,y1,z1]],down:[[x0,y0,z1],[x1,y0,z1],[x1,y0,z0],[x0,y0,z0]]})[face];
const r4=v=>Math.round(v*1e4)/1e4;
function fUV(face,lo,hi,f){const D=fCorners(face,lo,hi).map(f),eq=(a,b)=>Math.abs(a-b)<1e-6;
 for(let k=0;k<4;k++){const u=[0,1,2,3].map(j=>D[(j+k)%4]);if(eq(u[0][1],u[1][1])&&eq(u[1][0],u[2][0])&&eq(u[2][1],u[3][1])&&eq(u[3][0],u[0][0]))return[[u[0][0],u[0][1],u[2][0],u[2][1]].map(r4),k*90];}
 throw new Error('no uv solution for '+face);}
// Card in plane <n> = at; texture u runs from model coordinate a to b along axis ua, v likewise.
function fxCard(sprite,n,at,[ua,u0,u1],[va,v0,v1],uv=[0,0,16,16]){
 if(!fxTex[sprite])throw new Error('fxg sprite '+sprite+' missing from raiden_fx_textures.json');
 const N='xyz'.indexOf(n),U='xyz'.indexOf(ua),V='xyz'.indexOf(va),lo=[0,0,0],hi=[0,0,0];
 lo[N]=hi[N]=at;lo[U]=Math.min(u0,u1);hi[U]=Math.max(u0,u1);lo[V]=Math.min(v0,v1);hi[V]=Math.max(v0,v1);
 const from=lo.map(r4),to=hi.map(r4),f=p=>[uv[0]+(uv[2]-uv[0])*(p[U]-u0)/(u1-u0),uv[1]+(uv[3]-uv[1])*(p[V]-v0)/(v1-v0)];
 const faces={};for(const fc of FPAIR[n]){const[fuv,r]=fUV(fc,from,to,f);faces[fc]={texture:'#'+sprite,uv:fuv.map(v=>Math.min(16,Math.max(0,v))),...(r?{rotation:r}:{})};}
 return{from,to,shade:false,faces};}
const fxModel=(name,e)=>{MODELS[name]=e;for(const el of e)for(const v of[...el.from,...el.to])if(v<-16||v>32)throw new Error(name+': element outside the -16..32 model cube');
 const used=[...new Set(e.flatMap(el=>Object.values(el.faces).map(f=>f.texture.slice(1))))];
 const tex=Object.fromEntries(used.map(n=>[n,fxTex[n]]));
 json(path.join(assets,'models/item/raiden/judgment',name+'.json'),{ambientocclusion:false,textures:{...tex,particle:tex[used[0]]},elements:e});
 json(path.join(assets,'items/raiden/judgment',name+'.json'),{model:{type:'minecraft:model',model:'rlk:item/raiden/judgment/'+name}});};
// Blade halves: [y0, y1, centre x] following the curve c = 8.15 + 1.35 t^2.
const HALVES=[[BLADE.y0-.4,(BLADE.y0+BLADE.y1)/2+.3,8.15+1.35*.0625+1.1],[(BLADE.y0+BLADE.y1)/2-.3,Math.min(32,BLADE.y1+.35),8.15+1.35*.5625+.8]];
function bladeCards(sprite,width,{lean=0,depth=0,side=0,cross=0,z=8,mirror=false}={}){
 const e=[];HALVES.forEach(([y0,y1,cx],i)=>{const x=cx-lean+side,uv=mirror===(i%2===1)?[0,0,16,16]:[16,0,0,16];
  e.push(fxCard(sprite,'z',z+depth,['y',y0,y1],['x',x-width/2,x+width/2],uv));
  if(cross)e.push(fxCard(sprite,'x',x,['y',y0,y1],['z',8-cross/2,8+cross/2],uv));});return e;}
fxModel('blade_aura',[...bladeCards('glow_strip',4.2,{lean:.7,cross:1.6}),...bladeCards('blade_a',1.7,{lean:.9,depth:.04})]);
fxModel('blade_haze',bladeCards('glow_strip',8.4,{lean:.5,cross:3.2,depth:-.04}));
fxModel('blade_trail_near',bladeCards('blade_trail_a',4.4,{lean:.6,cross:1.4}));
fxModel('blade_trail_far',bladeCards('blade_trail_b',3.6,{lean:.5,cross:1.0}));
fxModel('blade_trail_faint',bladeCards('blade_trail_b',2.6,{lean:.4}));
for(let v=0;v<2;v++){const e=[];
 for(const s of[-1,1])e.push(...bladeCards(v?'bolt_c':'bolt_a',2.6,{side:s*1.7,depth:s*.35,mirror:s>0}));
 e.push(...bladeCards(v?'bolt_b':'bolt_d',2.2,{cross:2.4,lean:.3}).filter((_,i)=>i%2===1));
 fxModel('blade_lightning_'+v,e);}
// Quaternion helpers. Model coordinates are world-aligned; the final right-Y-pi
// correction cancels Minecraft's additional item-display model rotation.
const rad=x=>x*Math.PI/180;
const mul=(a,b)=>{const[x,y,z,w]=a,[X,Y,Z,W]=b;return[w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W,w*W-x*X-y*Y-z*Z];};
const q=e=>{const[x,y,z]=e.map(v=>rad(v)/2);return mul(mul([0,0,Math.sin(z),Math.cos(z)],[0,Math.sin(y),0,Math.cos(y)]),[Math.sin(x),0,0,Math.cos(x)]);};
const rot=(a,v)=>mul(mul(a,[...v,0]),[-a[0],-a[1],-a[2],a[3]]).slice(0,3);
const add=(a,b)=>a.map((v,i)=>v+b[i]),sub=(a,b)=>a.map((v,i)=>v-b[i]),times=(a,s)=>a.map(v=>v*s),lerp=(a,b,t)=>a.map((v,i)=>v+(b[i]-v)*t),dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0),norm=a=>times(a,1/Math.max(.00001,Math.hypot(...a))),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const clamp=x=>Math.max(0,Math.min(1,x)),smooth=x=>{x=clamp(x);return x*x*(3-2*x);};
function basisQuat(x,y,z){const m=[x[0],y[0],z[0],x[1],y[1],z[1],x[2],y[2],z[2]],tr=m[0]+m[4]+m[8];let a;if(tr>0){const s=Math.sqrt(tr+1)*2;a=[(m[7]-m[5])/s,(m[2]-m[6])/s,(m[3]-m[1])/s,s/4];}else if(m[0]>m[4]&&m[0]>m[8]){const s=Math.sqrt(1+m[0]-m[4]-m[8])*2;a=[s/4,(m[1]+m[3])/s,(m[2]+m[6])/s,(m[7]-m[5])/s];}else if(m[4]>m[8]){const s=Math.sqrt(1+m[4]-m[0]-m[8])*2;a=[(m[1]+m[3])/s,s/4,(m[5]+m[7])/s,(m[2]-m[6])/s];}else{const s=Math.sqrt(1+m[8]-m[0]-m[4])*2;a=[(m[2]+m[6])/s,(m[5]+m[7])/s,s/4,(m[3]-m[1])/s];}return norm(a);}

// ---- motion -----------------------------------------------------------------------------------------------------------
// Pattern ticks (rdTime of p15). HIT must be tenma.py p15's slash tick (tm/mg/strike 151 places the safe-dome hit, 152).
const T0=56,T_END=190,HIT=152,DOME_R=8,ARENA_R=24;
// Sky rift: the eye-shaped void (40 x 16 model units) at scale RIFT, tilted to face down toward the dome; from the flower
// it spans about 14..49 degrees above the horizon and 90 degrees across (the torn sky of the reference video).
const PORTAL=[0,10.2,-16],PORTAL_TILT=60,RIFT=13;
// The arm hangs from the shoulder half a block under the rift plane (its dark root sleeve reaches back into the void).
const SHOULDER=[0,9.6,-15.5],CAM=[0,1.6,3];
const ARM=5.2,L1=20/16*ARM,L2=22/16*ARM,HAND=6,SWORD=8.6;
const GRIP_OFF=[(GRIP[0]-8)/16,0,(GRIP[1]-8)/16];
const hullOf=name=>MODELS[name].flatMap(el=>{const P=[];for(const x of[el.from[0],el.to[0]])for(const y of[el.from[1],el.to[1]])for(const z of[el.from[2],el.to[2]])P.push([x/16-.5,y/16-.5,z/16-.5]);return P;});
const KATANA=hullOf('katana').filter(p=>p[1]>(13-8)/16);      // the blade (above the tsuba)
const atPose=(v,P)=>P.map(p=>add(v.t,rot(v.q,[p[0]*v.s[0],p[1]*v.s[1],p[2]*v.s[2]])));
const bladeFrame=(heading,elev)=>{const ph=rad(heading),be=rad(elev),d=[Math.sin(ph)*Math.cos(be),Math.sin(be),Math.cos(ph)*Math.cos(be)],edge=[Math.cos(ph),0,-Math.sin(ph)];return{d,edge,q:basisQuat(times(edge,-1),d,cross(d,edge))};};
// Contact: the grip on a circle of radius RG about the shoulder's vertical at height GH; the first heading (sweeping
// left -> right) at which the blade reaches the dome (within 0.12 b) is the contact heading.
const RG=4.5,GH=3.6,gripAt=th=>[SHOULDER[0]+RG*Math.sin(rad(th)),GH,SHOULDER[2]+RG*Math.cos(rad(th))];
const bladeGap=(g,th,el=0)=>Math.min(...atPose({t:g,q:bladeFrame(th,el).q,s:[SWORD,SWORD,SWORD]},KATANA).map(p=>Math.hypot(...p)))-DOME_R;
let TC=-80;while(bladeGap(gripAt(TC),TC)>.12&&TC<0)TC+=.05;
const GC=gripAt(TC);
// Keys: h = grip point, a = [heading, elevation] of the blade (heading 0 points at the player, -90 screen-left); hold =
// zero velocity; the others take Catmull-Rom tangents. The draw-back keys are the release's (shoulder-relative, x1.1).
const R=v=>add(SHOULDER,times(v,1.25)),HOLD=R([-6.0,-4.6,2.95]);
const keys=[
 {t:84,h:SHOULDER,a:[-80,80],hold:1},
 {t:106,h:R([-3.4,-1.85,1.65]),a:[-90,70]},
 {t:124,h:R([-6.2,-3.15,2.65]),a:[-96,38]},
 {t:136,h:R([-7.0,-4.35,3.15]),a:[-97,22]},
 {t:146,h:HOLD,a:[-100,17],hold:1},
 {t:149,h:lerp(HOLD,GC,.3),a:[-88,6]},
 {t:151,h:lerp(HOLD,GC,.75),a:[TC-26,2]},
 {t:HIT,h:GC,a:[TC,0],hold:1},
 {t:154,h:add(GC,[-.45,.5,-.3]),a:[TC-8,6]},
 {t:157,h:add(GC,[-.12,.12,-.08]),a:[TC-2.5,1.5]},
 {t:161,h:add(GC,[-1.3,1.4,-.7]),a:[TC-18,14]},
 {t:168,h:R([-4.2,-2.8,1.7]),a:[-62,45]},
 {t:178,h:R([-1.6,-.9,.7]),a:[-76,74]},
 {t:186,h:SHOULDER,a:[-80,85],hold:1}
];
function channel(name,t){const n=keys.length;if(t<=keys[0].t)return keys[0][name];if(t>=keys[n-1].t)return keys[n-1][name];
 let i=0;while(keys[i+1].t<=t)i++;const A=keys[i],B=keys[i+1],T=B.t-A.t,u=(t-A.t)/T;
 const tan=k=>{const K=keys[k];if(K.hold||k===0||k===n-1)return K[name].map(()=>0);return sub(keys[k+1][name],keys[k-1][name]).map(v=>v/(keys[k+1].t-keys[k-1].t));};
 const h00=2*u*u*u-3*u*u+1,h10=u*u*u-2*u*u+u,h01=-2*u*u*u+3*u*u,h11=u*u*u-u*u,m0=tan(i),m1=tan(i+1);
 return A[name].map((v,j)=>h00*v+h10*T*m0[j]+h01*B[name][j]+h11*T*m1[j]);}
// Two-bone arm with fixed segment lengths; the elbow bends toward a fixed pole on the player's left (it trails the cut).
function ik(s,w,a,b,pole){const v=sub(w,s),n=norm(v),D=Math.min(Math.max(Math.hypot(...v),Math.abs(a-b)+1e-4),(a+b)*.9995),x=(a*a-b*b+D*D)/(2*D),y=Math.sqrt(Math.max(0,a*a-x*x));let p=sub(pole,times(n,dot(pole,n)));if(Math.hypot(...p)<1e-3)p=cross(n,[1,0,0]);p=norm(p);return{elbow:add(s,add(times(n,x),times(p,y))),wrist:add(s,times(n,D)),short:Math.hypot(...v)-D};}
// Bone frame: local -Y runs from a to b, local -Z turns toward the player (tomoe discs outward).
function boneQ(a,b){const y=norm(sub(a,b));let f=sub(CAM,lerp(a,b,.5));f=sub(f,times(y,dot(f,y)));if(Math.hypot(...f)<.5)f=sub([0,1,0],times(y,y[1]));const z=times(norm(f),-1);return basisQuat(cross(y,z),y,z);}
let worstReach=0;
function rigAt(t){
 const size=smooth((t-84)/20)*(1-smooth((t-174)/12)),tense=smooth((t-136)/8)*(1-smooth(t-145));
 // a short tense tremble while the blade is held back, a shudder against the dome after the hit
 const shake=tense*.07+(t>HIT&&t<162?.05:0);
 const h=add(channel('h',t),times([Math.sin(t*2.9),Math.sin(t*4.1+1),Math.sin(t*3.3+2)],shake)),[heading,elev]=add(channel('a',t),[Math.sin(t*3.7)*1.2*tense,0]);
 const {d,edge,q:swordQ}=bladeFrame(heading,elev);
 if(size<.0001)return{size:0,upper:[SHOULDER,[0,0,0,1]],forearm:[SHOULDER,[0,0,0,1]],hand:[SHOULDER,[0,0,0,1]],sword:[SHOULDER,swordQ],d,edge};
 const pole=norm([-1,0,.45]),handFrame=sol=>{let F=norm(sub(sol.wrist,sol.elbow));F=norm(add(sub(F,times(d,dot(F,d))),times(edge,.5)));const X=times(F,-1);return basisQuat(X,d,cross(X,d));};
 let wrist=add(h,[0,size,0]),sol,handQ;
 for(let it=0;it<6;it++){sol=ik(SHOULDER,wrist,L1*size,L2*size,pole);handQ=handFrame(sol);wrist=sub(h,rot(handQ,times(GRIP_OFF,HAND*size)));}
 sol=ik(SHOULDER,wrist,L1*size,L2*size,pole);handQ=handFrame(sol);if(size>.99)worstReach=Math.max(worstReach,sol.short);
 const grip=add(sol.wrist,rot(handQ,times(GRIP_OFF,HAND*size)));
 return{size,upper:[SHOULDER,boneQ(SHOULDER,sol.elbow)],forearm:[sol.elbow,boneQ(sol.elbow,sol.wrist)],hand:[sol.wrist,handQ],sword:[grip,swordQ],d,edge};
}
const parts={rift_void:'rift_void',rift_depth:'rift_depth',rift_haze:'rift_haze',rift_edge:'rift_edge_0',rift_edge_glow:'rift_edge_glow',rift_stars:'rift_stars',rift_iris:'rift_iris',rift_fragments:'rift_fragments',upper:'upper_arm',forearm:'forearm',hand:'closed_hand',upper_veins:'upper_veins',forearm_veins:'forearm_veins',sword:'katana',blade_aura:'blade_aura',blade_haze:'blade_haze',blade_lightning:'blade_lightning_0',trail1:'blade_trail_near',trail2:'blade_trail_far',trail3:'blade_trail_faint'};
const scaled=([t,q],s)=>({t,q,s:[s,s,s]});
function sword(t){const r=rigAt(t);return scaled(r.sword,SWORD*r.size);}
function pose(t){
 // the sky splits (a thin slit T0..T0+14, then it gapes open to +22) and collapses with the dome's shatter (178..188)
 const opening=smooth((t-T0)/14),openHeight=.035+.965*smooth((t-T0-6)/16),closing=1-smooth((t-178)/10),pulse=1+.025*Math.sin(t*.34),portalQ=q([PORTAL_TILT,0,0]),o={};
 const k=RIFT*closing,portalScale=[k*opening,k*openHeight,k];
 for(const n of ['rift_void','rift_depth','rift_haze','rift_edge','rift_edge_glow','rift_stars','rift_iris','rift_fragments'])o[n]={t:[...PORTAL],q:[...portalQ],s:[...portalScale]};
 o.rift_depth.t=add(PORTAL,rot(portalQ,[0,0,-.06]));
 o.rift_haze.t=add(PORTAL,rot(portalQ,[0,0,-.12]));o.rift_haze.s=times(portalScale,1.10*pulse);
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
 // afterimages of the cut, only while the blade is fast (HIT-5 .. HIT)
 for(let i=1;i<=3;i++){o['trail'+i]=sword(t-i*.65);if(t<HIT-5||t>HIT)o['trail'+i].s=[0,0,0];}
 return o;
}

// ---- checks: never below the floor, no solid part inside the dome, the cut reaches the dome on HIT ---------------------
const HULL=Object.fromEntries(Object.values(parts).map(m=>[m,hullOf(m)]));
const SOLID=['upper','forearm','hand','sword'];
let low=1e9,inDome=1e9,far=0;
for(let t=T0;t<=T_END;t++){const p=pose(t);
 for(const n of Object.keys(parts)){if(Math.max(...p[n].s)<1e-4)continue;const W=atPose(p[n],HULL[p[n].model?p[n].model.replace(/_\d$/,'_0'):parts[n]]);
  low=Math.min(low,...W.map(w=>w[1]));if(SOLID.includes(n)){inDome=Math.min(inDome,...W.map(w=>Math.hypot(...w)));far=Math.max(far,...W.map(w=>Math.hypot(w[0],w[2])));}}}
if(low<.05)throw new Error(`a judgment part reaches y ${low.toFixed(2)} (below the floor)`);
if(inDome<DOME_R-.25)throw new Error(`a solid judgment part enters the dome (distance ${inDome.toFixed(2)} < ${DOME_R})`);
const hitGap=bladeGap(rigAt(HIT).sword[0],TC);
if(Math.abs(hitGap)>.3)throw new Error(`the blade misses the dome on HIT (gap ${hitGap.toFixed(2)})`);

// ---- functions: start (summon on the execution yaw), key frames, tick (as the boss), cleanup ----------------------------
// A key frame at tick k sets the pose of the next key and interpolates to it, so the client lands on every key on time.
const KEYS=[T0+1,62,70,78,84,92,100,108,116,124,132,140,146,147,148,149,150,151,152,153,154,155,157,160,163,167,172,177,182,186];
const f=v=>(Math.abs(v)<.0000005?0:v).toFixed(5).replace(/\.?0+$/,'')+'f',arr=a=>'['+a.map(f).join(',')+']';
const nbt=v=>`{translation:${arr(v.t)},left_rotation:${arr(v.q)},scale:${arr(v.s)},right_rotation:[0f,1f,0f,0f]}`;
const sel=n=>`@e[type=item_display,tag=rlk_rd_j_${n},limit=1]`;
const previous={},first=pose(T0);
for(const n of Object.keys(parts))previous[n]=[...first[n].q];
KEYS.forEach((k,i)=>{const nxt=i+1<KEYS.length?KEYS[i+1]:T_END,p=pose(nxt),lines=[`# Key ${k}: the pose of ${nxt}, interpolated over ${nxt-k} t.`];
 for(const n of Object.keys(parts)){if(dot(p[n].q,previous[n])<0)p[n].q=times(p[n].q,-1);previous[n]=[...p[n].q];
  lines.push(`data merge entity ${sel(n)} {interpolation_duration:${nxt-k},start_interpolation:0,transformation:${nbt(p[n])}${p[n].model?`,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/judgment/${p[n].model}"}}`:''}}`);}
 fn('frame/'+k,lines);});
fn('cleanup',['# Removes the rift and the arm.','kill @e[type=item_display,tag=rlk_rd_judgment_rig]']);
const TAGS=n=>`"rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_tm","rlk_rd_judgment_rig","rlk_rd_j_new","rlk_rd_j_${n}"`;
fn('start',[`# At the arena centre, facing the player (tenma.py p15, rdTime ${T0}): the rift and the arm, ${Object.keys(parts).length} displays on the execution yaw.`,
 'function rlk:boss/raiden/judgment_rig/cleanup',
 ...Object.entries(parts).map(([n,asset])=>`summon minecraft:item_display ~ ~ ~ {Tags:[${TAGS(n)}],billboard:"fixed",item_display:"none",brightness:{block:15,sky:15},view_range:4f,shadow_radius:0f,width:0f,height:0f,teleport_duration:0,interpolation_duration:1,transformation:${nbt(first[n])},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/judgment/${asset}"}}}`),
 'execute rotated ~ 0 run tp @e[type=item_display,tag=rlk_rd_j_new] ~ ~ ~ ~ 0','tag @e[type=item_display,tag=rlk_rd_j_new] remove rlk_rd_j_new']);
// the clash: where the blade touches the dome on HIT (rig frame = ^left ^up ^forward of the parts' yaw), just outside it
const hitPts=atPose(pose(HIT).sword,KATANA),touch=hitPts.reduce((a,b)=>Math.hypot(...b)<Math.hypot(...a)?b:a),CLASH=times(touch,(DOME_R+.3)/Math.hypot(...touch));
fn('clash',[`# @s = the boss on ${HIT} with the dome raised (tenma.py tm/mg/slash): the burst where the katana strikes the dome.`,
 `execute at ${sel('sword')} rotated as ${sel('sword')} positioned ^${f(CLASH[0]).slice(0,-1)} ^${f(CLASH[1]).slice(0,-1)} ^${f(CLASH[2]).slice(0,-1)} run function rlk:boss/raiden/fx/mangeop_clash`]);
// dispatcher: a guard every 6 keys keeps a tick to at most ~14 checks
const disp=[`# @s = the boss during 만겁 (tenma.py p15, rdTime ${T0+1}..${T_END}): the key frames, then the cleanup.`,`execute if score @s rdTime matches ${T_END}.. run return run function rlk:boss/raiden/judgment_rig/cleanup`];
KEYS.forEach((k,i)=>{if(i&&i%6===0)disp.push(`execute if score @s rdTime matches ..${k-1} run return 0`);disp.push(`execute if score @s rdTime matches ${k} run return run function rlk:boss/raiden/judgment_rig/frame/${k}`);});
fn('tick',disp);
for(const [n,e] of Object.entries(MODELS))if(e.length>900)throw new Error(`judgment model ${n}: ${e.length} elements`);
const debugDp=arg('--debug-dp')&&path.resolve(arg('--debug-dp'));
if(debugDp){
 const D=path.join(debugDp,'data/rlk/function');fs.rmSync(path.join(D,'rd_dbg/mg'),{recursive:true,force:true});
 fs.cpSync(FN_DIR,path.join(D,'boss/raiden/judgment_rig'),{recursive:true});
 for(let t=T0;t<=T_END;t++){const p=pose(t);put(path.join(D,'rd_dbg/mg',t+'.mcfunction'),Object.keys(parts).map(n=>`data merge entity ${sel(n)} {interpolation_duration:0,start_interpolation:0,transformation:${nbt(p[n])},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/judgment/${p[n].model||parts[n]}"}}}`).join('\n'));}
}
const hit=rigAt(HIT),tip=add(hit.sword[0],times(hit.d,(BLADE.y1-8)/16*SWORD));
console.log(`Built the 만겁 rift + arm: ${Object.keys(parts).length} displays, ${Object.keys(MODELS).length} models (${Object.values(MODELS).reduce((a,e)=>a+e.length,0)} elements), ${KEYS.length} key frames ${T0}..${T_END}; `+
 `the cut meets the dome on ${HIT} at heading ${TC.toFixed(1)} (grip ${GC.map(v=>v.toFixed(2))}, tip ${tip.map(v=>v.toFixed(2))}); lowest point y ${low.toFixed(2)}, nearest solid ${inDome.toFixed(2)} b from the dome centre, farthest ${far.toFixed(1)} b; arm reach shortfall ${worstReach.toFixed(3)}.`);
