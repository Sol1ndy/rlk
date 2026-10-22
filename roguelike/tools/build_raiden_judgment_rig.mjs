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
// r 8 about the origin. Rift opens T0.., the arm emerges 84.., draws the katana back to the left and holds 146, sweeps it
// about 220 degrees left -> right in front of the player (147..160; one key frame per tick), low over the arena outside
// the dome and over the dome as it crosses the player's front on HIT (the lethal slash, the clash), follows through far
// to the right (160), withdraws slowly into the rift by 186 and the rift collapses with the dome's shatter (176 -> 188).
// Nothing goes below the floor (hidden = scale 0 at the shoulder, never a teleport) and no solid part enters the dome,
// in the exact poses and in what the client shows between key frames (all checked here).
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
// Afterimages of the cut (user 10-22: the arc must read): ghost blades of soft light, wide, uniform along the blade
// (the tip moves fastest), with a faint edge crackle on the nearest ones; five of them fan out behind the blade.
fxModel('blade_trail_near',[...bladeCards('glow_strip',8.0,{lean:.6,cross:2.4}),...bladeCards('blade_a',1.5,{lean:.9,depth:.04})]);
fxModel('blade_trail_far',bladeCards('glow_strip',7.0,{lean:.5,cross:1.6}));
fxModel('blade_trail_faint',bladeCards('glow_strip',5.5,{lean:.4}));
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
// User 10-22 ("갑주 팔이 나와서 베는게 아니라 그냥 톡 치고 들어가는데"): the 10-22a restoration cut only 70 degrees (from
// heading -100 to -30, still on the player's left), stopped dead on the dome's edge, shuddered there and recoiled up and
// back, with 4-8 t between the key frames of the recoil (forearm / hand turning 63-73 degrees per key). It read as a
// poke. Now the arm draws the katana far back to the left (146), then sweeps it about 220 degrees left -> right in
// front of the player (147..160; 200 degrees in 148..158, up to 31 degrees per tick with one key frame per tick, so no
// display turns more than about 40 degrees between two keys and the client's shortest-path slerp follows the arc):
// with the arm nearly straight, low over the arena floor outside the dome at the sides and over the dome's top as it
// crosses the player's front on HIT (the clash; the dome lifts the blade if it would touch), then it follows through
// far to the right and up (160), five afterimage cards trail the blade along the arc, and the arm withdraws slowly up
// into the rift (to 186). The checks below run on the exact poses AND on the poses the client shows between key frames
// (translation / scale lerp, rotation slerp).
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
const bladeGap=(g,th,el=0)=>Math.min(...atPose({t:g,q:bladeFrame(th,el).q,s:[SWORD,SWORD,SWORD]},KATANA).map(p=>Math.hypot(...p)))-DOME_R;
// The dome deflects the blade: at a grip point g and heading th the elevation is raised just enough that the blade
// passes CLEAR blocks outside the dome (CLEAR covers the chord the client cuts between two per-tick key frames).
const CLEAR=.45,lift=(g,th,el)=>{let e=el;while(bladeGap(g,th,e)<CLEAR&&e<75)e+=.25;return e;};
// Keys: h = grip point, a = [heading, elevation] of the blade before the lift (heading 0 points at the player, -90
// screen-left, +90 screen-right); hold = zero velocity; the others take Catmull-Rom tangents. During the cut the grip
// runs a wide arc with the arm nearly straight: low and far out at the sides (3.6 b up, 10-11 b off the shoulder's
// vertical), up over the dome's front in the middle (8 b up, 6.6 b in front of the flower), so the whole arm swings with
// the blade; the blade is cocked back at the start, in line at the middle, trailing at the end, and stays inside the
// arena wall (or above its top) at the sides.
const R=v=>add(SHOULDER,times(v,1.25));
const HOLD=[-9.5,5.5,-17.5];
const keys=[
 {t:84,h:SHOULDER,a:[-80,80],p:[-1,0,.45],hold:1},
 {t:106,h:R([-3.4,-1.85,1.65]),a:[-92,70],p:[-1,0,.45]},
 {t:124,h:R([-6.0,-3.0,1.4]),a:[-100,46],p:[-1,.2,.45]},
 {t:136,h:R([-7.2,-3.4,-.6]),a:[-104,40],p:[-1,.3,.4]},
 {t:146,h:HOLD,a:[-106,38],p:[-1,.4,.3],hold:1},
 {t:147,h:[-10.4,4.4,-15.0],a:[-103,27],p:[-1,.45,.3]},
 {t:148,h:[-10.4,3.8,-12.2],a:[-90,30],p:[-1,.5,.3]},
 {t:149,h:[-9.2,3.8,-9.6],a:[-70,6],p:[-.9,.5,.5]},
 {t:150,h:[-7.0,5.6,-8.4],a:[-52,2],p:[-.7,.5,.8]},
 {t:151,h:[-3.6,8.0,-7.8],a:[-24,2],p:[-.35,.5,1]},
 {t:HIT,h:[.3,8.9,-7.8],a:[6,0],p:[0,.5,1]},
 {t:153,h:[4.0,8.0,-8.0],a:[36,2],p:[.35,.5,1]},
 {t:154,h:[7.2,5.6,-8.6],a:[62,2],p:[.7,.5,.8]},
 {t:155,h:[9.0,3.6,-10.2],a:[80,6],p:[.9,.5,.5]},
 {t:156,h:[10.6,3.6,-12.6],a:[94,28],p:[1,.5,.3]},
 {t:157,h:[10.4,4.0,-15.2],a:[104,38],p:[1,.45,.3]},
 {t:158,h:[9.9,4.6,-17.0],a:[110,44],p:[1,.4,.3]},
 {t:160,h:[9.4,5.2,-18.2],a:[114,48],p:[1,.4,.3],hold:1},
 {t:165,h:R([4.2,-2.6,1.2]),a:[108,56],p:[1,.3,.35]},
 {t:170,h:R([2.8,-1.6,1.0]),a:[100,66],p:[.9,.2,.4]},
 {t:176,h:R([1.4,-.8,.6]),a:[90,74],p:[.8,.1,.45]},
 {t:182,h:R([.4,-.2,.2]),a:[84,82],p:[.8,0,.45]},
 {t:186,h:SHOULDER,a:[80,85],p:[.8,0,.45],hold:1}];
function channel(name,t){const n=keys.length;if(t<=keys[0].t)return keys[0][name];if(t>=keys[n-1].t)return keys[n-1][name];
 let i=0;while(keys[i+1].t<=t)i++;const A=keys[i],B=keys[i+1],T=B.t-A.t,u=(t-A.t)/T;
 const tan=k=>{const K=keys[k];if(K.hold||k===0||k===n-1)return K[name].map(()=>0);return sub(keys[k+1][name],keys[k-1][name]).map(v=>v/(keys[k+1].t-keys[k-1].t));};
 const h00=2*u*u*u-3*u*u+1,h10=u*u*u-2*u*u+u,h01=-2*u*u*u+3*u*u,h11=u*u*u-u*u,m0=tan(i),m1=tan(i+1);
 return A[name].map((v,j)=>h00*v+h10*T*m0[j]+h01*B[name][j]+h11*T*m1[j]);}
// Two-bone arm with fixed segment lengths; the elbow bends toward the keyed pole `p` (on the player's left while the arm
// emerges and winds up, turning over the top to the right through the cut, so the elbow trails the hand and the forearm
// stays high over the dome while the hand passes in front of it).
function ik(s,w,a,b,pole){const v=sub(w,s),n=norm(v),D=Math.min(Math.max(Math.hypot(...v),Math.abs(a-b)+1e-4),(a+b)*.9995),x=(a*a-b*b+D*D)/(2*D),y=Math.sqrt(Math.max(0,a*a-x*x));let p=sub(pole,times(n,dot(pole,n)));if(Math.hypot(...p)<1e-3)p=cross(n,[1,0,0]);p=norm(p);return{elbow:add(s,add(times(n,x),times(p,y))),wrist:add(s,times(n,D)),short:Math.hypot(...v)-D};}
// Bone frame: local -Y runs from a to b, local X is the normal of the arm's bend plane (shoulder, elbow, wrist: N; it
// points the same way for both bones), so local -Z (the tomoe discs) lies in that plane. Both bones lie in it, so the
// frame is defined and continuous however the arm turns (a camera-facing twist flipped the upper arm whenever a bone
// pointed at the player: 75..170 degrees between two key frames of the sweep).
function boneQ(a,b,N){const y=norm(sub(a,b)),x=norm(sub(N,times(y,dot(N,y))));return basisQuat(x,y,cross(x,y));}
function bendFrame(s,sol,pole){const n=norm(sub(sol.wrist,s));let o=sub(sub(sol.elbow,s),times(n,dot(sub(sol.elbow,s),n)));
 if(Math.hypot(...o)<.05)o=sub(pole,times(n,dot(pole,n)));o=norm(o);return{N:norm(cross(n,o)),out:o};}
// The lift as a function of the heading during the cut: the elevation each heading of the sweep needs (with the grip it
// has there), dilated by +-LIFT_W degrees, so a blade the client slerps between two key frames up to 31 degrees apart
// stays lifted all the way across the dome (a lift sampled only at the key ticks would let the chord dip into it).
const LIFT_A=146,LIFT_B=162,LIFT_W=18;
let NEED=null;
const needAt=th=>{if(!NEED){NEED=[];for(let t=LIFT_A;t<=LIFT_B;t+=.05){const h=channel('h',t),[hd,el]=channel('a',t);NEED.push([hd,lift(h,hd,-30)]);}}
 let e=-90;for(const [hd,el] of NEED)if(Math.abs(hd-th)<=LIFT_W)e=Math.max(e,el);return e;};
// The withdrawal: from RET the arm keeps the pose it has there (no IK while it shrinks) and draws back into the
// shoulder as `size` falls to 0 (174..186), drifting up into the rift; the joints cannot flip while it collapses.
const RET=170;
let worstReach=0;
function rigAt(t){
 if(t>RET){const r=rigCore(RET),k=(1-smooth((t-174)/12))*1,up=[0,.9*smooth((t-RET)/16),0],to=v=>add(add(SHOULDER,times(sub(v,SHOULDER),k)),times(up,1-k*0)),r2=structuredClone(r);
  r2.size=k;for(const n of['upper','forearm','hand','sword'])r2[n]=[to(r[n][0]),r[n][1]];return r2;}
 return rigCore(t);
}
function rigCore(t){
 const size=smooth((t-84)/20)*(1-smooth((t-174)/12)),tense=smooth((t-136)/8)*(1-smooth(t-145));
 // a short tense tremble while the blade is held back, a shudder through the arm as the dome deflects the blade
 const shake=tense*.07+(t>HIT&&t<156?.04:0);
 const h=add(channel('h',t),times([Math.sin(t*2.9),Math.sin(t*4.1+1),Math.sin(t*3.3+2)],shake));
 const heading=channel('a',t)[0]+Math.sin(t*3.7)*1.2*tense,base=channel('a',t)[1];
 const elev=size<.5?base:t>=LIFT_A&&t<=LIFT_B?Math.max(base,needAt(heading)):lift(h,heading,base);
 const {d,edge,q:swordQ}=bladeFrame(heading,elev);
 if(size<.0001)return{size:0,upper:[SHOULDER,[0,0,0,1]],forearm:[SHOULDER,[0,0,0,1]],hand:[SHOULDER,[0,0,0,1]],sword:[SHOULDER,swordQ],d,edge,heading,elev};
 // the fist's frame: local -X along the forearm, projected off the blade; through the cut it is biased toward the edge
 // (the wrist on the spine side, no flip as the blade swings round), the bias fades out after the follow-through,
 // where the withdrawing forearm arrives from the edge side and would cancel it
 const bias=.5*(1-smooth((t-158)/6));
 const pole=norm(channel('p',t)),handFrame=sol=>{let F=norm(sub(sol.wrist,sol.elbow));F=norm(add(sub(F,times(d,dot(F,d))),times(edge,bias)));const X=times(F,-1);return basisQuat(X,d,cross(X,d));};
 let wrist=add(h,[0,size,0]),sol,handQ;
 for(let it=0;it<6;it++){sol=ik(SHOULDER,wrist,L1*size,L2*size,pole);handQ=handFrame(sol);wrist=sub(h,rot(handQ,times(GRIP_OFF,HAND*size)));}
 sol=ik(SHOULDER,wrist,L1*size,L2*size,pole);handQ=handFrame(sol);if(size>.99)worstReach=Math.max(worstReach,sol.short);
 const grip=add(sol.wrist,rot(handQ,times(GRIP_OFF,HAND*size)));
 const B=bendFrame(SHOULDER,sol,pole);
 return{size,upper:[SHOULDER,boneQ(SHOULDER,sol.elbow,B.N)],forearm:[sol.elbow,boneQ(sol.elbow,sol.wrist,B.N)],hand:[sol.wrist,handQ],sword:[grip,swordQ],d,edge,heading,elev};
}
// Five afterimages of the blade (lags in ticks), shown while the blade is fast (CUT_A .. CUT_B): they fan out behind it
// along the arc of the cut.
const TRAILS=[[.45,'blade_trail_near'],[.9,'blade_trail_near'],[1.4,'blade_trail_far'],[2.0,'blade_trail_far'],[2.7,'blade_trail_faint']];
const CUT_A=147,CUT_B=158;
const parts={rift_void:'rift_void',rift_depth:'rift_depth',rift_haze:'rift_haze',rift_edge:'rift_edge_0',rift_edge_glow:'rift_edge_glow',rift_stars:'rift_stars',rift_iris:'rift_iris',rift_fragments:'rift_fragments',upper:'upper_arm',forearm:'forearm',hand:'closed_hand',upper_veins:'upper_veins',forearm_veins:'forearm_veins',sword:'katana',blade_aura:'blade_aura',blade_haze:'blade_haze',blade_lightning:'blade_lightning_0',...Object.fromEntries(TRAILS.map(([,m],i)=>['trail'+(i+1),m]))};
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
 // afterimages: hidden (scale 0, at the blade) outside the fast part of the cut
 TRAILS.forEach(([lag],i)=>{const n='trail'+(i+1);o[n]=t>=CUT_A&&t<=CUT_B?sword(t-lag):{...sword(t),s:[0,0,0]};});
 return o;
}

// ---- key frames and the client's view of them -------------------------------------------------------------------------
// A key frame at tick k sets the pose of the next key and interpolates to it, so the client lands on every key on time.
// One key per tick through the cut (145..162); every 2 t in the recoil, every 4 t while the arm emerges. The first key is
// 2 t after the summon (the client must tick a new display before its first interpolation, kit TRAVEL_GAP).
const KEYS=[];for(let k=T0+2;k<84;k+=4)KEYS.push(k);for(let k=84;k<145;k+=4)KEYS.push(k);for(let k=145;k<=162;k++)KEYS.push(k);
for(let k=164;k<=176;k+=2)KEYS.push(k);KEYS.push(179,182,186);
const slerp=(a,b,u)=>{let c=dot(a,b);const s=c<0?-1:1;c=Math.abs(c);if(1-c<1e-6)return norm(a.map((v,i)=>v+(s*b[i]-v)*u));const om=Math.acos(Math.min(1,c)),so=Math.sin(om),k0=Math.sin((1-u)*om)/so,k1=s*Math.sin(u*om)/so;return a.map((v,i)=>k0*v+k1*b[i]);};
const POSE={};const poseAt=t=>POSE[t]??=pose(t);
// what the client shows at (fractional) tick t: the display left key k_i at pose(k_i) and moves to pose(k_i+1)
function clientPose(t){const ks=[T0,...KEYS,T_END];let i=0;while(i+1<ks.length&&ks[i+1]<=t)i++;if(i+1>=ks.length)return poseAt(T_END);
 const k0=ks[i],k1=ks[i+1],A=i===0?poseAt(T0):poseAt(k0),B=poseAt(k1),u=i===0?0:(t-k0)/(k1-k0),o={};
 for(const n of Object.keys(parts))o[n]={t:lerp(A[n].t,B[n].t,u),q:slerp(A[n].q,B[n].q,u),s:lerp(A[n].s,B[n].s,u),model:(u<1?A:B)[n].model};return o;}

// ---- checks: never below the floor, no solid part inside the dome (exact and client view), small key steps, the cut ----
const HULL=Object.fromEntries(Object.values(parts).map(m=>[m,hullOf(m)]));
const SOLID=['upper','forearm','hand','sword'];
let low=1e9,inDome=1e9,far=0,cLow=1e9,cInDome=1e9,tipDev=0,wallHit=0;
const scan=(p,acc)=>{for(const n of Object.keys(parts)){if(Math.max(...p[n].s)<1e-4)continue;const W=atPose(p[n],HULL[p[n].model?p[n].model.replace(/_\d$/,'_0'):parts[n]]);
  acc.low=Math.min(acc.low,...W.map(w=>w[1]));if(SOLID.includes(n)){acc.dome=Math.min(acc.dome,...W.map(w=>Math.hypot(...w)));acc.far=Math.max(acc.far,...W.map(w=>Math.hypot(w[0],w[2])));
   // the arena wall (r 24 about the arena centre = the rig origin, 6 b high): the blade may pass over it, not into it
   if(n==='sword')wallHit=Math.max(wallHit,...W.filter(w=>w[1]<6.5).map(w=>Math.hypot(w[0],w[2])));}}};
const tipOf=v=>add(v.t,rot(v.q,[0,(BLADE.y1-8)/16*v.s[1],0]));
for(let t=T0;t<=T_END;t++){const a={low:1e9,dome:1e9,far:0};scan(poseAt(t),a);low=Math.min(low,a.low);inDome=Math.min(inDome,a.dome);far=Math.max(far,a.far);}
for(let t=T0;t<=T_END;t+=.25){const c={low:1e9,dome:1e9,far:0},cp=clientPose(t);scan(cp,c);cLow=Math.min(cLow,c.low);cInDome=Math.min(cInDome,c.dome);
 if(t>=CUT_A-1&&t<=CUT_B+2)tipDev=Math.max(tipDev,Math.hypot(...sub(tipOf(cp.sword),tipOf(pose(t).sword))));}
if(wallHit>23.5)throw new Error(`the katana reaches into the arena wall (r ${wallHit.toFixed(1)} below its top)`);
if(Math.min(low,cLow)<.05)throw new Error(`a judgment part reaches y ${Math.min(low,cLow).toFixed(2)} (below the floor)`);
if(Math.min(inDome,cInDome)<DOME_R-.1)throw new Error(`a solid judgment part enters the dome (distance ${Math.min(inDome,cInDome).toFixed(2)} < ${DOME_R}; client view ${cInDome.toFixed(2)})`);
let stepMax=[0,''];for(const n of Object.keys(parts)){let prev=poseAt(T0)[n];for(const k of KEYS){const p=poseAt(k===KEYS.at(-1)?T_END:KEYS[KEYS.indexOf(k)+1])[n];
 if(Math.max(...p.s)>1e-4&&Math.max(...prev.s)>1e-4){const a=2*Math.acos(Math.min(1,Math.abs(dot(p.q,prev.q))))*180/Math.PI;if(a>stepMax[0])stepMax=[a,`${n} key ${k}`];}prev=p;}}
if(stepMax[0]>60)throw new Error(`a display turns ${stepMax[0].toFixed(1)} deg between two key frames (${stepMax[1]}): the client's shortest-path slerp would cut the arc`);
const H=t=>rigAt(t).heading,sweep=H(158)-H(148),sweepAll=H(160)-H(146);
if(sweep<150||!(H(HIT-1)<0&&H(HIT)>=0))throw new Error(`the cut is too short or misses the player's front on ${HIT} (148..158: ${sweep.toFixed(0)} deg; ${H(HIT-1).toFixed(0)} -> ${H(HIT).toFixed(0)})`);
const hitGap=bladeGap(rigAt(HIT).sword[0],rigAt(HIT).heading,rigAt(HIT).elev);
if(hitGap>1.2)throw new Error(`the blade does not meet the dome on HIT (gap ${hitGap.toFixed(2)})`);

// ---- functions: start (summon on the execution yaw), key frames, tick (as the boss), cleanup ----------------------------
const f=v=>(Math.abs(v)<.0000005?0:v).toFixed(5).replace(/\.?0+$/,'')+'f',arr=a=>'['+a.map(f).join(',')+']';
const nbt=v=>`{translation:${arr(v.t)},left_rotation:${arr(v.q)},scale:${arr(v.s)},right_rotation:[0f,1f,0f,0f]}`;
const sel=n=>`@e[type=item_display,tag=rlk_rd_j_${n},limit=1]`;
const previous={},first=poseAt(T0);
for(const n of Object.keys(parts))previous[n]=[...first[n].q];
KEYS.forEach((k,i)=>{const nxt=i+1<KEYS.length?KEYS[i+1]:T_END,p=structuredClone(poseAt(nxt)),lines=[`# Key ${k}: the pose of ${nxt}, interpolated over ${nxt-k} t.`];
 for(const n of Object.keys(parts)){if(dot(p[n].q,previous[n])<0)p[n].q=times(p[n].q,-1);previous[n]=[...p[n].q];
  lines.push(`data merge entity ${sel(n)} {interpolation_duration:${nxt-k},start_interpolation:0,transformation:${nbt(p[n])}${p[n].model?`,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/judgment/${p[n].model}"}}`:''}}`);}
 fn('frame/'+k,lines);});
fn('cleanup',['# Removes the rift and the arm.','kill @e[type=item_display,tag=rlk_rd_judgment_rig]']);
const TAGS=n=>`"rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_tm","rlk_rd_judgment_rig","rlk_rd_j_new","rlk_rd_j_${n}"`;
fn('start',[`# At the arena centre, facing the player (tenma.py p15, rdTime ${T0}): the rift and the arm, ${Object.keys(parts).length} displays on the execution yaw.`,
 'function rlk:boss/raiden/judgment_rig/cleanup',
 ...Object.entries(parts).map(([n,asset])=>`summon minecraft:item_display ~ ~ ~ {Tags:[${TAGS(n)}],billboard:"fixed",item_display:"none",brightness:{block:15,sky:15},view_range:4f,shadow_radius:0f,width:0f,height:0f,teleport_duration:0,interpolation_duration:1,transformation:${nbt(first[n])},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/judgment/${asset}"}}}`),
 'execute rotated ~ 0 run tp @e[type=item_display,tag=rlk_rd_j_new] ~ ~ ~ ~ 0','tag @e[type=item_display,tag=rlk_rd_j_new] remove rlk_rd_j_new']);
// the clash: where the blade comes nearest the dome on HIT (rig frame = ^left ^up ^forward of the parts' yaw), just outside it
const hitPts=atPose(poseAt(HIT).sword,KATANA),touch=hitPts.reduce((a,b)=>Math.hypot(...b)<Math.hypot(...a)?b:a),CLASH=times(touch,(DOME_R+.3)/Math.hypot(...touch));
fn('clash',[`# @s = the boss on ${HIT} with the dome raised (tenma.py tm/mg/slash): the burst where the katana is deflected over the dome.`,
 `execute at ${sel('sword')} rotated as ${sel('sword')} positioned ^${f(CLASH[0]).slice(0,-1)} ^${f(CLASH[1]).slice(0,-1)} ^${f(CLASH[2]).slice(0,-1)} run function rlk:boss/raiden/fx/mangeop_clash`]);
// dispatcher: a guard every 6 keys keeps a tick to at most ~14 checks
const disp=[`# @s = the boss during 만겁 (tenma.py p15, rdTime ${T0+1}..${T_END}): the key frames, then the cleanup.`,`execute if score @s rdTime matches ${T_END}.. run return run function rlk:boss/raiden/judgment_rig/cleanup`];
KEYS.forEach((k,i)=>{if(i&&i%6===0)disp.push(`execute if score @s rdTime matches ..${k-1} run return 0`);disp.push(`execute if score @s rdTime matches ${k} run return run function rlk:boss/raiden/judgment_rig/frame/${k}`);});
fn('tick',disp);
for(const [n,e] of Object.entries(MODELS))if(e.length>900)throw new Error(`judgment model ${n}: ${e.length} elements`);
const debugDp=arg('--debug-dp')&&path.resolve(arg('--debug-dp'));
if(debugDp){
 // rd_dbg/mg/<t>: the exact pose of tick t; rd_dbg/mgc/<t>[h]: what the client shows at t (and t + 0.5) between keys
 const D=path.join(debugDp,'data/rlk/function');fs.rmSync(path.join(D,'rd_dbg/mg'),{recursive:true,force:true});fs.rmSync(path.join(D,'rd_dbg/mgc'),{recursive:true,force:true});
 fs.cpSync(FN_DIR,path.join(D,'boss/raiden/judgment_rig'),{recursive:true});
 const dump=(p,file)=>put(path.join(D,file),Object.keys(parts).map(n=>`data merge entity ${sel(n)} {interpolation_duration:0,start_interpolation:0,transformation:${nbt(p[n])},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/judgment/${p[n].model||parts[n]}"}}}`).join('\n'));
 const path_=[];for(let t=140;t<=190;t+=.25){const e=pose(t).sword,c=clientPose(t).sword;path_.push({t,hilt:e.t,tip:tipOf(e),ctip:tipOf(c),chilt:c.t});}
 put(path.join(debugDp,'mg_path.json'),JSON.stringify(path_));
 for(let t=T0;t<=T_END;t++){dump(poseAt(t),`rd_dbg/mg/${t}.mcfunction`);dump(clientPose(t),`rd_dbg/mgc/${t}.mcfunction`);dump(clientPose(t+.5),`rd_dbg/mgc/${t}h.mcfunction`);}
}
const hit=rigAt(HIT),tip=add(hit.sword[0],times(hit.d,(BLADE.y1-8)/16*SWORD));
console.log(`Built the 만겁 rift + arm: ${Object.keys(parts).length} displays, ${Object.keys(MODELS).length} models (${Object.values(MODELS).reduce((a,e)=>a+e.length,0)} elements), ${KEYS.length} key frames ${T0}..${T_END}; `+
 `the cut sweeps ${sweepAll.toFixed(0)} deg (146 -> 160; ${sweep.toFixed(0)} deg in 148..158), crosses the player's front on ${HIT} (heading ${hit.heading.toFixed(1)}, elevation ${hit.elev.toFixed(1)} deg over the dome, gap ${hitGap.toFixed(2)}; tip ${tip.map(v=>v.toFixed(2))}); `+
 `largest key step ${stepMax[0].toFixed(1)} deg (${stepMax[1]}); lowest y ${Math.min(low,cLow).toFixed(2)}, nearest solid ${inDome.toFixed(2)} b from the dome centre (client view ${cInDome.toFixed(2)}), farthest ${far.toFixed(1)} b; client tip deviation ${tipDev.toFixed(2)} b; arm reach shortfall ${worstReach.toFixed(3)}.`);
