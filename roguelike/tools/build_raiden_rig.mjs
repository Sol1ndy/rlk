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
const rigDir=path.join(dp,'data/rlk/function/boss/raiden/rig');
// Every file under rig/ is generated here: start clean so retimed clips leave no stale ticks.
fs.rmSync(rigDir,{recursive:true,force:true});
const fn=(n,s)=>put(path.join(rigDir,n+'.mcfunction'),Array.isArray(s)?s.join('\n'):s);
const swatch=n=>'rlk:raiden/fx/'+n;
// Concrete/metal keys serve the normal-phase weapons and encounter objects. The armoured
// Baleful Shadowlord uses the shared opaque swatches from build_raiden_materials.py.
const textures={skin:'rlk:raiden/skin',white:'rlk:player_motion/white_concrete',silver:'rlk:player_motion/light_gray_concrete',dark:'rlk:player_motion/black_concrete',purple:'rlk:player_motion/purple_concrete',blue:'rlk:player_motion/blue_concrete',light:'rlk:player_motion/light_blue_concrete',gold:'rlk:cm/fm/metal',
 lilac:swatch('arm_lilac'),shade:swatch('arm_shade'),deep:swatch('arm_deep'),tomoe:swatch('arm_tomoe'),gdull:swatch('gold_dull'),bpale:swatch('blade_pale'),bedge:swatch('blade_edge'),bcore:swatch('blade_core'),grip:swatch('grip_dark'),hdull:swatch('hand_dull'),hdark:swatch('hand_dull_dark'),nail:swatch('nail_glow')};
const faces=['north','south','east','west','up','down'];
const box=(from,to,tex,overrides={})=>({from,to,faces:Object.fromEntries(faces.map(f=>[f,{texture:'#'+(overrides[f]||tex),uv:[0,0,16,16]}]))});
const model=(name,elements)=>{json(path.join(assets,'models/item/raiden',name+'.json'),{ambientocclusion:false,textures:{...textures,particle:textures.purple},elements});json(path.join(assets,'items/raiden',name+'.json'),{model:{type:'minecraft:model',model:'rlk:item/raiden/'+name}});};
// Same geometry, every face tinted by one constant multiplier (item definition tints).
const DULL_TINT=0xA098AC;
const tinted=(name,elements,tint=DULL_TINT)=>{json(path.join(assets,'models/item/raiden',name+'.json'),{ambientocclusion:false,textures:{...textures,particle:textures.purple},elements:elements.map(e=>({...e,faces:Object.fromEntries(Object.entries(e.faces).map(([k,f])=>[k,{...f,tintindex:0}]))}))});json(path.join(assets,'items/raiden',name+'.json'),{model:{type:'minecraft:model',model:'rlk:item/raiden/'+name,tints:[{type:'minecraft:constant',value:tint}]}});};
// A left-hand copy: x -> 16-x with east/west faces exchanged.
const mirrorX=els=>els.map(e=>({from:[16-e.to[0],e.from[1],e.from[2]],to:[16-e.from[0],e.to[1],e.to[2]],faces:Object.fromEntries(Object.entries(e.faces).map(([k,f])=>[k==='east'?'west':k==='west'?'east':k,f]))}));
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
// Raiden herself is drawn desaturated/dark while the armour carries her (<part>_dull).
for(const[n,[a,b,uv,over,start,end,inf]]of Object.entries(bodySpecs)){const els=[sb(a,b,uv,start,end),sb(a,b,over,start,end,inf)];model(n,els);tinted(n+'_dull',els);}
if(arg('--skin')){fs.mkdirSync(path.join(assets,'textures/raiden'),{recursive:true});fs.copyFileSync(arg('--skin'),path.join(assets,'textures/raiden/skin.png'));}

// ---- Baleful Shadowlord armour --------------------------------------------------------
// All pieces remain within the native model cube bounds. Larger forms use display transforms.
// Shared model conventions (pixels, display pivot at 8,8,8):
//  * arm segments hang along -Y from their joint; -Z is the outward (front) face.
//  * hands hang from the wrist along -Y; +Z is the palm, -Z the back, the thumb sits at
//    model -X: the authored hand is a RIGHT hand and every *_l model is its mirror.
//  * blades point along +Y; model -X is the cutting edge (convex side of the curve) and
//    +X the spine. The rig poses blades by (tip, edge) frames so every cut leads with -X.
// Flat disc emblem on one face: arm_tomoe field, dull-gold rim and three gold commas.
function face2d(dir,c,[u0,u1],[v0,v1],[d0,d1],tex){
 const at={'-z':(u,v,d)=>[c[0]+u,c[1]+v,c[2]-d],'+z':(u,v,d)=>[c[0]-u,c[1]+v,c[2]+d],'-x':(u,v,d)=>[c[0]-d,c[1]+v,c[2]-u],'+x':(u,v,d)=>[c[0]+d,c[1]+v,c[2]+u]}[dir];
 const a=at(u0,v0,d0),b=at(u1,v1,d1);return box(a.map((x,i)=>Math.min(x,b[i])),a.map((x,i)=>Math.max(x,b[i])),tex);
}
function tomoe(c,r,dir='-z'){
 const disc=(R,d,tex)=>[[R,.42*R],[.42*R,R],[.72*R,.72*R]].map(([a,b])=>face2d(dir,c,[-a,a],[-b,b],d,tex));
 const e=[...disc(r,[-.05,.2],'gdull'),...disc(.74*r,[-.05,.34],'tomoe')];
 for(let i=0;i<3;i++){const a=Math.PI/2+i*2*Math.PI/3,b=a+.8,h=.16*r,t=.1*r,x=Math.cos(a)*.34*r,y=Math.sin(a)*.34*r,u=Math.cos(b)*.56*r,v=Math.sin(b)*.56*r;
  e.push(face2d(dir,c,[x-h,x+h],[y-h,y+h],[0,.48],'gdull'),face2d(dir,c,[u-t,u+t],[v-t,v+t],[0,.44],'gdull'));}
 return e;
}
// Pale lilac puppet plates, shaded sides, deep-violet joints, dull-gold trims, tomoe discs.
const plate={east:'shade',west:'shade',south:'shade'};
model('puppet_upper',[box([5.8,-4,5.8],[10.2,8,10.2],'deep'),box([5.2,-2.6,5.2],[10.8,6.4,10.8],'lilac',plate),box([5.0,5.3,5.0],[11.0,6.3,11.0],'gdull'),box([5.0,-2.5,5.0],[11.0,-1.5,11.0],'gdull'),box([5.3,6.4,5.3],[10.7,9.3,10.7],'deep',{up:'shade'}),box([5.0,7.4,5.0],[11.0,8.1,11.0],'gdull'),box([5.1,1.3,5.1],[10.9,1.75,10.9],'deep'),...tomoe([8,3.85,5.2],1.95),...tomoe([8,3.85,10.8],1.6,'+z')]);
model('puppet_forearm',[box([5.8,-6,5.8],[10.2,8,10.2],'deep'),box([5.3,-4.8,5.3],[10.7,5.9,10.7],'lilac',plate),box([5.0,4.7,5.0],[11.0,5.8,11.0],'gdull'),box([5.0,-4.8,5.0],[11.0,-3.8,11.0],'gdull'),box([5.4,5.8,5.4],[10.6,8.5,10.6],'deep'),box([5.1,-1.85,5.1],[10.9,-1.4,10.9],'deep'),box([7.55,-3.6,10.6],[8.45,4.5,10.95],'deep'),...tomoe([8,1.75,5.3],1.75)]);
function puppetHand(kind){
 const e=[box([4.2,1.8,6.4],[11.8,8.3,9.6],'lilac',{south:'shade',east:'shade',west:'shade',down:'deep'}),box([4.0,6.9,6.1],[12.0,8.4,9.9],'gdull'),box([4.25,1.35,6.2],[11.75,2.25,9.8],'deep'),...tomoe([8,4.6,6.4],1.75)];
 for(let i=0;i<4;i++){const x=4.55+i*1.85;
  if(kind==='closed')e.push(box([x,-.5,6.25],[x+1.45,2.5,10.35],'lilac',{east:'shade',west:'shade'}),box([x,-.5,9.5],[x+1.45,3.3,11.0],'shade'),box([x,-.8,6],[x+1.45,.1,7],'deep'));
  else if(kind==='open'){const end=[-3.7,-5,-4.6,-3.1][i];e.push(box([x,end+1.5,6.6],[x+1.4,2.2,9.1],'lilac',{east:'shade',west:'shade'}),box([x-.05,end+1.0,6.45],[x+1.45,end+1.6,9.25],'deep'),box([x+.1,end,6.75],[x+1.3,end+1.1,8.95],'shade'),box([x+.25,end-.45,6.95],[x+1.15,end+.05,8.75],'gdull'));}
  else{const end=[-2.6,-3.5,-3.3,-2.3][i],dx=(i-1.5)*.4;e.push(box([x+dx*.5,end+1.3,6.6],[x+1.4+dx*.5,2.2,9.1],'lilac',{east:'shade',west:'shade'}),box([x+dx-.05,end+.8,6.9],[x+dx+1.45,end+1.5,9.6],'deep'),box([x+dx,end-1.2,8.2],[x+dx+1.4,end+1.0,10.6],'shade'),box([x+dx+.3,end-2.0,9.6],[x+dx+1.1,end-1.0,11.2],'gdull'));}
 }
 e.push(box([2.5,2.0,6.7],[4.7,6.7,9.2],'lilac',{west:'shade',south:'shade'}),box([1.7,kind==='closed'?1.3:.1,7.1],[3.6,3.8,9.4],'shade'),box([1.9,kind==='closed'?.9:-.4,7.4],[3.4,kind==='closed'?1.4:.2,9.1],'gdull'));
 return e;
}
for(const kind of['open','closed','claw']){const els=puppetHand(kind);model('puppet_hand_'+kind,els);model('puppet_hand_'+kind+'_l',mirrorX(els));}
// Two large dull bronze-grey hands carry Raiden from below: dedicated chunky geometry,
// fingers curled toward the palm, glowing violet nails and faint seams.
const dullSide={east:'hdark',west:'hdark'};
model('support_upper',[box([5.6,-4,5.6],[10.4,8,10.4],'hdark'),box([5.0,-2.8,5.0],[11.0,6.6,11.0],'hdull',{...dullSide,south:'hdark'}),box([4.8,5.5,4.8],[11.2,6.6,11.2],'hdark'),box([4.8,-2.8,4.8],[11.2,-1.8,11.2],'hdark'),box([5.2,6.6,5.2],[10.8,9.4,10.8],'hdark'),box([7.7,-1.4,4.82],[8.3,5.2,5.02],'nail')]);
model('support_forearm',[box([5.6,-6,5.6],[10.4,8,10.4],'hdark'),box([4.9,-4.6,4.9],[11.1,6.0,11.1],'hdull',{...dullSide,south:'hdark'}),box([4.7,4.9,4.7],[11.3,6.0,11.3],'hdark'),box([4.7,-4.8,4.7],[11.3,-3.7,11.3],'hdark'),box([5.3,6.0,5.3],[10.7,8.6,10.7],'hdark'),box([7.7,-3.4,4.72],[8.3,4.6,4.92],'nail'),box([4.72,-.8,7.7],[4.92,3.2,8.3],'nail')]);
function supportHand(){
 const e=[box([4.5,6.4,5.5],[11.5,10.2,10.5],'hdark'),box([3.4,.6,5.8],[12.6,7.0,10.2],'hdull',dullSide),box([3.55,-.3,5.45],[12.45,1.5,7.1],'hdark'),box([4.6,2.0,5.5],[11.4,5.6,5.85],'hdark'),box([5.0,3.3,10.15],[11.0,3.75,10.4],'hdark'),box([7.6,.9,10.15],[8.05,6.4,10.4],'hdark')];
 for(let i=0;i<4;i++){const x=3.6+i*2.3,w=1.95,y=.6-[3.3,4.0,3.8,3.0][i];
  e.push(box([x,y,5.9],[x+w,.8,9.3],'hdull',dullSide),box([x-.05,y-.2,5.75],[x+w+.05,y+.6,9.45],'hdark'),box([x+.1,y-2.3,7.1],[x+w-.1,y,10.5],'hdull',dullSide),box([x+.35,y-3.0,8.6],[x+w-.35,y-1.9,10.8],'nail'));}
 e.push(box([1.3,1.3,6.6],[3.5,5.9,9.9],'hdull',{...dullSide,south:'hdark'}),box([.8,-1.1,7.6],[3.0,1.5,10.9],'hdull',dullSide),box([1.05,-1.9,8.9],[2.75,-.8,11.1],'nail'));
 return e;
}
model('support_hand_r',supportHand());model('support_hand_l',mirrorX(supportHand()));

// Normal katana: violet body, white cutting edge on -X, violet spine on +X, gilded guard.
function katana(){const e=[box([7.3,1.8,7.25],[8.7,10,8.75],'dark'),box([7.05,2,7.05],[8.95,2.75,8.95],'gold')];for(let y=3;y<9;y+=1.55)e.push(box([7.12,y,7.12],[8.88,y+.62,8.88],'purple'));e.push(box([4.4,9.0,6.75],[11.6,10.15,9.25],'gold'),box([6,8.8,6.2],[10,10.3,9.8],'purple'));for(let i=0;i<14;i++){const y=10+i*1.51,curve=i*i*.0065,width=1.65-i*.075;e.push(box([7.9+curve-width/2,y,7.5],[7.9+curve+width/2,y+1.61,8.5],'purple',{north:'light',south:'blue'}),box([7.88+curve-width/2,y,7.43],[8.10+curve-width/2,y+1.62,8.57],'white'));}return e;}
model('katana',katana());
// The Shadowlord's pale violet katana. The blade bows toward +X (spine), so the convex -X
// side carries the continuous white cutting edge; a violet fuller runs beside the spine on
// both flats. Dark grip with dull-gold wraps, tsuba and habaki.
function giantKatana(){
 const e=[box([7.2,1.4,7.2],[8.8,9.7,8.8],'grip'),box([6.95,.45,6.95],[9.05,1.45,9.05],'gdull')];
 for(let y=2.3;y<9.2;y+=1.5)e.push(box([7.1,y,7.1],[8.9,y+.45,8.9],'gdull'));
 e.push(box([5.0,9.7,6.4],[11.0,10.4,9.6],'gdull'),box([5.7,9.7,5.7],[10.3,10.4,10.3],'gdull'),box([6.3,9.62,6.8],[9.7,10.48,9.2],'deep'),box([6.85,10.4,7.2],[9.2,11.5,8.8],'gdull'));
 const y0=11.5,N=16,h=(31.4-y0)/N;
 for(let i=0;i<N;i++){const t=i/(N-1),y=y0+h*i,c=8+1.3*t*t,base=2.7-.75*t,w=i<N-2?base:i===N-2?1.25:.6,xr=c+base/2,xl=xr-w,edge=Math.min(.65,w*.5);
  e.push(box([xl,y,7.6],[xl+edge,y+h+.01,8.4],'bedge'),box([xl+edge-.1,y,7.42],[xr,y+h+.01,8.58],'bpale',{east:'bcore'}));
  if(i<N-3)e.push(box([xr-.95,y,7.35],[xr-.42,y+h+.01,8.65],'bcore'));}
 return e;
}
model('giant_katana',giantKatana());
// ---- Painted lightning cards -------------------------------------------------------------
// Weapon, palm and chakra lightning (and the death splinters) are painted gradient sprites
// (rlk:raiden/fxg/*, tools/build_raiden_fx_textures.py; catalogue tools/raiden_fx_textures.json)
// on a few flat cards: zero-thickness elements with a face on both sides, shade off, uv in
// 0..16, element rotation about one axis by 0/+-22.5/+-45 degrees only, coordinates -16..32.
// Each effect keeps its model name and is still one display sharing the attached weapon's or
// hand's pivot, quaternion and scale, so the datapack's flicker/charge/release logic is unchanged.
const fxCatalogue=JSON.parse(fs.readFileSync(path.join(here,'raiden_fx_textures.json'),'utf8'));
const fxSprite=Object.fromEntries(fxCatalogue.textures.map(t=>[t.name,t]));
const FACE_PAIR={x:['east','west'],y:['up','down'],z:['south','north']};
const r4=v=>Math.round(v*1e4)/1e4;
// Corners TL, TR, BR, BL of a face seen from outside (vanilla face vertex order).
function faceCorners(face,[x0,y0,z0],[x1,y1,z1]){return{north:[[x1,y1,z0],[x0,y1,z0],[x0,y0,z0],[x1,y0,z0]],south:[[x0,y1,z1],[x1,y1,z1],[x1,y0,z1],[x0,y0,z1]],east:[[x1,y1,z1],[x1,y1,z0],[x1,y0,z0],[x1,y0,z1]],west:[[x0,y1,z0],[x0,y1,z1],[x0,y0,z1],[x0,y0,z0]],up:[[x0,y1,z0],[x1,y1,z0],[x1,y1,z1],[x0,y1,z1]],down:[[x0,y0,z1],[x1,y0,z1],[x1,y0,z0],[x0,y0,z0]]}[face];}
// Face uv [u1,v1,u2,v2] + rotation so every corner shows fn(corner): corner i takes the
// (i - rotation/90)-th entry of (u1v1, u2v1, u2v2, u1v2), as vanilla does.
function solveUV(face,lo,hi,fn){const D=faceCorners(face,lo,hi).map(fn),eq=(a,b)=>Math.abs(a-b)<1e-6;
 for(let k=0;k<4;k++){const u=[0,1,2,3].map(j=>D[(j+k)%4]);if(eq(u[0][1],u[1][1])&&eq(u[1][0],u[2][0])&&eq(u[2][1],u[3][1])&&eq(u[3][0],u[0][0]))return[[u[0][0],u[0][1],u[2][0],u[2][1]].map(r4),k*90];}
 throw new Error('no uv solution for '+face);}
// One card in the plane <n> = at. u/v = [axis, a, b]: the texture's uv[0] -> uv[2] runs from model
// coordinate a to b along that axis (b < a mirrors), likewise v. rot = [axis, angle] about the centre.
function card(sprite,n,at,[ua,u0,u1],[va,v0,v1],{uv=[0,0,16,16],rot=null}={}){
 if(!fxSprite[sprite])throw new Error(`fxg sprite ${sprite} is not in raiden_fx_textures.json (run build_raiden_fx_textures.py)`);
 const N='xyz'.indexOf(n),U='xyz'.indexOf(ua),V='xyz'.indexOf(va),lo=[0,0,0],hi=[0,0,0];
 lo[N]=hi[N]=at;lo[U]=Math.min(u0,u1);hi[U]=Math.max(u0,u1);lo[V]=Math.min(v0,v1);hi[V]=Math.max(v0,v1);
 const from=lo.map(r4),to=hi.map(r4);
 if([...from,...to].some(c=>c<-16||c>32))throw new Error(`card ${sprite} leaves -16..32: ${from} ${to}`);
 const fn=p=>[uv[0]+(uv[2]-uv[0])*(p[U]-u0)/(u1-u0),uv[1]+(uv[3]-uv[1])*(p[V]-v0)/(v1-v0)];
 const faces={};for(const f of FACE_PAIR[n]){const[fuv,r]=solveUV(f,from,to,fn);faces[f]={texture:'#'+sprite,uv:fuv.map(v=>Math.min(16,Math.max(0,v))),...(r?{rotation:r}:{})};}
 const el={from,to,shade:false,faces};
 if(rot&&rot[1]){if(![-45,-22.5,22.5,45].includes(rot[1]))throw new Error('card rotation '+rot[1]);el.rotation={origin:from.map((v,i)=>r4((v+to[i])/2)),axis:rot[0],angle:rot[1]};}
 return el;
}
// uv sub-range of a sprite laid along [a, b] when the whole sprite spans [A, B] (for split cards).
const span=(a,b,A,B)=>[16*(a-A)/(B-A),16*(b-A)/(B-A)];
const segments=(a,b,n)=>Array.from({length:n},(_,i)=>[a+(b-a)*i/n,a+(b-a)*(i+1)/n]);
const meanOver=(f,a,b,n=24)=>{let s=0;for(let i=0;i<=n;i++)s+=f(a+(b-a)*i/n);return s/(n+1);};
const smoothstep=(a,b,x)=>{const t=Math.min(1,Math.max(0,(x-a)/(b-a)));return t*t*(3-2*t);};
function fxModel(name,elements,tint=null){
 const used=[...new Set(elements.flatMap(e=>Object.values(e.faces).map(f=>f.texture.slice(1))))];
 const tex=Object.fromEntries(used.map(n=>[n,fxSprite[n].texture]));
 const els=tint===null?elements:elements.map(e=>({...e,faces:Object.fromEntries(Object.entries(e.faces).map(([k,f])=>[k,{...f,tintindex:0}]))}));
 json(path.join(assets,'models/item/raiden',name+'.json'),{ambientocclusion:false,textures:{...tex,particle:tex[used[0]]},elements:els});
 json(path.join(assets,'items/raiden',name+'.json'),{model:{type:'minecraft:model',model:'rlk:item/raiden/'+name,...(tint===null?{}:{tints:[{type:'minecraft:constant',value:tint}]})}});
}
// Blade lightning is shared by the normal katana and the giant katana (which it is painted to):
// x/z follow the display's power scale about the pivot, y (length) never scales. The bright
// edge bolt sits just outside the cutting edge (model -X), a thinner crackle along the spine.
const bladeOutline=y=>{const t=Math.min(1,Math.max(0,(y-11.5)/19.9)),c=8+1.3*t*t,hb=(2.7-.75*t)/2;return[c-hb+smoothstep(28.4,31.4,y)*(2*hb-.6),c+hb];};
const bladeMid=y=>{const[a,b]=bladeOutline(y);return(a+b)/2;};
function bladeLightning(spear=false,variant=0,trail=false){
 const e=[],ab='ab'[variant],ba='ba'[variant];
 if(spear){
  // Leaf spear head y 18..31.3: a bolt beside each edge, one crossed card through the head.
  const i=y=>Math.min(7.6,Math.max(0,(y-18)/1.65)),mid=y=>8+i(y)**2*.025,hw=y=>(2.2-.24*i(y))/2,Y0=17.6,Y1=31.8;
  if(trail){
   e.push(card('blade_trail_'+ab,'z',8,['y',Y1,Y0],['x',meanOver(mid,Y0,Y1)-2.4,meanOver(mid,Y0,Y1)+2.4]));
   e.push(card('blade_trail_'+ba,'x',meanOver(mid,Y0,Y1),['y',Y1,Y0],['z',5.6,10.4]));
   return e;
  }
  for(const[side,z]of[[-1,7.85],[1,8.15]])for(const[k,[a,b]]of segments(Y0,Y1,2).entries()){
   const x=meanOver(y=>mid(y)+side*(hw(y)+.3),a,b),[u0,u1]=span(a,b,Y0,Y1);
   e.push(card('blade_'+'abc'[(k+variant+(side>0?1:0))%3],'z',z,['y',a,b],['x',x-1.6*side,x+1.6*side],{uv:[u0,0,u1,16]}));
  }
  e.push(card('blade_c','x',meanOver(mid,Y0,Y1),['y',Y0,Y1],variant?['z',10.2,5.8]:['z',5.8,10.2]));
  return e;
 }
 if(trail){
  // Afterimage ribbons: afterglow streaks along the old blade line, brightest at the tip
  // (blade_trail u=0 is the newest end), in the blade plane and crossed for edge-on views.
  const Y0=10,Y1=31.6;
  for(const[a,b]of segments(Y0,Y1,2)){const x=meanOver(bladeMid,a,b),[u0,u1]=span(Y1-b,Y1-a,0,Y1-Y0);
   e.push(card('blade_trail_'+ab,'z',8,['y',b,a],['x',x-2.8,x+2.8],{uv:[u0,0,u1,16]}));
   e.push(card('blade_trail_'+ba,'x',x,['y',b,a],['z',5.4,10.6],{uv:[u0,0,u1,16]}));}
  return e;
 }
 // The painted sheath in the blade plane: the blade body hides its middle, leaving the edge
 // bolt, its outward forks, the spine crackle and the tip fork around the steel.
 const sh=fxSprite['rig_katana_'+ab].card;
 e.push(card('rig_katana_'+ab,'z',8,['y',...sh.model_y],['x',...sh.model_x]));
 // Crossed cards through the same edge bolt (three straight pieces of one continuous blade_*
 // sprite following the curve) and the spine crackle, read when the blade is seen edge-on.
 const E0=9.9,E1=31.7;
 for(const[a,b]of segments(E0,E1,3)){const[u0,u1]=span(a,b,E0,E1);
  e.push(card('blade_'+ab,'x',meanOver(y=>bladeOutline(y)[0]-.38,a,b),['y',a,b],variant?['z',10.4,5.6]:['z',5.6,10.4],{uv:[u0,0,u1,16]}));}
 const S0=10.6,S1=30.6;
 for(const[a,b]of segments(S0,S1,2)){const[u0,u1]=span(a,b,S0,S1);
  e.push(card('rim_crackle_'+ba,'x',meanOver(y=>bladeOutline(y)[1]+.32,a,b),['y',a,b],['z',6.2,9.8],{uv:[u0,0,u1,16]}));}
 return e;
}
for(const kind of['katana','polearm'])for(const variant of[0,1]){
 fxModel(`fx_weapon/${kind}_${variant}`,bladeLightning(kind==='polearm',variant));
 fxModel(`fx_weapon/${kind}_trail_${variant}`,bladeLightning(kind==='polearm',variant,true));
}
// Palm lightning in hand-model space (fingers along -Y, palm +Z, back -Z with the tomoe disc).
// Charge: arcs from the fingertips and thumb converge into the palm, on the palm side and
// (mirrored) on the back, with a small crackling seal. Focus: the same arcs, a tighter seal and a
// small hot core. Release: a radiating crown on both sides plus one crossed card through the hand.
// The centre never becomes a solid ball: the hand stays readable.
function palmLightning(closed=false,stage='charge',variant=0){
 const e=[],pc=fxSprite.rig_palm.card,[X0,X1]=pc.model_x,[Y0,Y1]=pc.model_y,[cx,cy]=pc.centre;
 // Clear of the palm (z 9.6), the curled fingers of the fist (z 11) and the tomoe disc (z 5.92).
 const front=closed?11.45:10.05,back=5.5,yTip=closed?-1.6:Y0,mirror=m=>m?{uv:[16,0,0,16]}:{};
 if(stage==='release'){
  const R=8.4,c=[8,3.8],flip=variant?{uv:[16,16,0,0]}:{};
  e.push(card('rig_crown','z',front+.4,['x',c[0]-R,c[0]+R],['y',c[1]+R,c[1]-R],flip));
  e.push(card('rig_crown','z',back-.4,['x',c[0]+R,c[0]-R],['y',c[1]+R,c[1]-R],flip));
  e.push(card('rig_crown','x',8,['z',8-R,8+R],['y',c[1]-R,c[1]+R],flip));
  return e;
 }
 e.push(card('rig_palm','z',front,['x',X0,X1],['y',Y1,yTip],mirror(variant)));
 e.push(card('rig_palm','z',back,['x',X0,X1],['y',Y1,yTip],mirror(1-variant)));
 const r=(stage==='focus'?1.3:2.2)/.8;
 e.push(card('chakra_'+'ab'[variant],'z',front+.4,['x',cx-r,cx+r],['y',cy+r,cy-r]));
 if(stage==='focus')e.push(card('orb_core','z',front+.8,['x',cx-1.7,cx+1.7],['y',cy+1.7,cy-1.7]));
 return e;
}
for(const form of['open','closed'])for(const phase of['charge','focus','release'])for(const variant of[0,1])fxModel(`fx_weapon/palm_${form}_${phase}_${variant}`,palmLightning(form==='closed',phase,variant));
// Chakra: sparse arcs leaping along the outside of the rim, a couple of outward forks and
// rising sparks; the ring's centre (Raiden's face) stays empty. In front of the ring (model -Z).
// A card is placed radially at angle phi (multiple of 22.5 deg): authored on the nearest
// axis and turned about Z through its own centre by the remaining 0/+-22.5/+-45 degrees.
function rimCard(sprite,phi,rIn,rOut,width,z,mirrored){
 const base=Math.round(phi/90)*90,rho=phi-base,b=(base%360+360)%360,a=phi*Math.PI/180,d=(rIn+rOut)/2,c=[8+d*Math.cos(a),8+d*Math.sin(a)];
 const R=b%180===0?0:1,T=1-R,out=b<180?1:-1,len=(rOut-rIn)/2,w=(mirrored?-1:1)*width/2;
 // sprite v=0 (arc apex / bolt top) points outward, v=1 sits on the rim
 return card(sprite,'z',z,['xy'[T],c[T]-w,c[T]+w],['xy'[R],c[R]+out*len,c[R]-out*len],{rot:['z',rho]});
}
function chakraLightning(variant){
 const e=[],arcs=[22.5,112.5,202.5,292.5].map(p=>p+45*variant),forks=[157.5,337.5].map(p=>p+45*variant),sparks=[67.5,247.5].map(p=>p+45*variant);
 // arc sprite: ends at (0.06,0.86) and (0.94,0.86), apex at v~0.2. Ends on r=15.6, 40 deg apart.
 const re=15.6,half=20*Math.PI/180,dc=re*Math.cos(half),W=2*re*Math.sin(half)/.88,H=(19.2-dc)/.66;
 arcs.forEach((phi,i)=>e.push(rimCard('arc_'+'ab'[(i+variant)%2],phi,dc-.14*H,dc+.86*H,W,6.6,i>1)));
 forks.forEach((phi,i)=>e.push(rimCard('vbolt_'+'abc'[(i+variant)%3],phi,14.6,21.6,2.2,6.35,i===1)));
 sparks.forEach((phi,i)=>e.push(rimCard('charge_spark',phi,15.0,19.6,2.4,6.1,i===1)));
 return e;
}
for(const variant of[0,1])fxModel(`fx_weapon/chakra_${variant}`,chakraLightning(variant));
const spear=[box([7.4,-15.5,7.4],[8.6,18.2,8.6],'dark')];for(const y of[-12,-5,2,9,16])spear.push(box([7.16,y,7.16],[8.84,y+.7,8.84],'gold'));for(let i=0;i<8;i++){const y=18+i*1.65,w=2.2-i*.24,x=8+i*i*.025;spear.push(box([x-w/2,y,7.45],[x+w/2,y+1.72,8.55],'purple',{north:'light',east:'white'}));}spear.push(box([5.6,16,6.8],[10.4,18,9.2],'gold'),box([6.5,-15.8,6.5],[9.5,-14.6,9.5],'purple'));model('polearm',spear);

// Halo: deep-violet ring with dull-gold studs, pale fuller dots, lilac ticks and three tomoe.
const ring=[];for(let i=0;i<64;i++){const a=i*Math.PI/32,x=8+13.6*Math.cos(a),y=8+13.6*Math.sin(a);ring.push(box([x-.75,y-.75,7.4],[x+.75,y+.75,8.6],i%8===0?'gdull':i%2?'deep':'shade'));if(i%2===0)ring.push(box([8+12.3*Math.cos(a)-.42,8+12.3*Math.sin(a)-.42,7.65],[8+12.3*Math.cos(a)+.42,8+12.3*Math.sin(a)+.42,8.35],'bcore'));}for(let i=0;i<12;i++){const a=i*Math.PI/6,x=8+16*Math.cos(a),y=8+16*Math.sin(a);ring.push(box([x-.65,y-1.5,7.8],[x+.65,y+1.5,8.2],i%3===0?'gdull':'lilac'));}for(let l=0;l<3;l++){const a=l*Math.PI*2/3;for(let i=0;i<8;i++){const b=a+i*.16,x=8+6.2*Math.cos(b),y=8+6.2*Math.sin(b);ring.push(box([x-.6,y-.6,7.6],[x+.6,y+.6,8.4],'shade'));}}for(const d of[90,210,330]){const a=d*Math.PI/180,x=8+13.6*Math.cos(a),y=8+13.6*Math.sin(a);ring.push(...tomoe([x,y,7.4],1.9),...tomoe([x,y,8.6],1.9,'+z'));}model('chakra',ring);
model('armor',[box([3.5,5.7,5.4],[12.5,8.1,10.6],'lilac',plate),box([3.3,5.2,5.2],[12.7,6.15,10.8],'gdull'),box([5.1,-4.1,5.5],[10.9,-2,10.5],'deep'),box([4.4,-3.9,5.25],[11.6,-3,10.75],'gdull'),box([6.85,.6,5.1],[9.15,5.3,5.45],'lilac'),...tomoe([8,3.0,5.1],1.55),box([3.2,-7.0,7],[5.3,-2.9,10.3],'deep'),box([10.7,-7,7],[12.8,-2.9,10.3],'deep'),box([3.0,-7.3,6.8],[5.5,-6.6,10.5],'gdull'),box([10.5,-7.3,6.8],[13,-6.6,10.5],'gdull')]);
model('crown',[box([3.65,12,3.75],[12.35,13.1,12.25],'gdull'),box([3.6,12.35,3.7],[12.4,12.75,12.3],'deep'),box([3,13,5.2],[4.2,18.8,7.4],'deep',{north:'shade'}),box([2.7,17.6,5.1],[4.5,19.3,7.5],'lilac'),box([11.8,13,5.2],[13,18.8,7.4],'deep',{north:'shade'}),box([11.5,17.6,5.1],[13.3,19.3,7.5],'lilac'),box([6.3,12.2,3.45],[9.7,15.5,3.75],'deep'),...tomoe([8,13.85,3.45],1.55)]);
const ribbon=[box([6.4,-9,8.2],[9.6,8,9.15],'deep',{north:'lilac'}),box([6.4,-9,8.1],[7.0,8,9.25],'gdull'),box([9.0,-9,8.1],[9.6,8,9.25],'gdull'),box([6.1,-11,8.2],[9.9,-8,9.15],'deep',{north:'shade'}),box([6.9,-1,8.05],[9.1,.4,9.3],'shade')];model('ribbon',ribbon);tinted('ribbon_dull',ribbon);
model('electro_orb',[box([4.5,12,4.5],[11.5,19,11.5],'purple'),box([5.2,12.7,3.9],[10.8,18.3,12.1],'light'),box([3.9,12.7,5.2],[12.1,18.3,10.8],'light'),box([6.7,10.9,6.7],[9.3,20.1,9.3],'white'),box([-.8,14.9,6.8],[3.5,16.1,9.2],'gold'),box([12.5,14.9,6.8],[16.8,16.1,9.2],'gold'),box([6.8,14.9,-.8],[9.2,16.1,3.5],'purple'),box([6.8,14.9,12.5],[9.2,16.1,16.8],'purple')]);
const flower=[box([4.5,8,4.5],[11.5,9.5,11.5],'gold'),box([6,9.5,6],[10,17,10],'purple'),box([6.6,13,6.6],[9.4,19.8,9.4],'light')];for(let i=0;i<6;i++){const a=i*Math.PI/3;for(let s=0;s<4;s++){const r=3+s*1.5,x=8+Math.cos(a)*r,z=8+Math.sin(a)*r,y=13+s*.85;flower.push(box([x-1.4,y-.6,z-1.4],[x+1.4,y+1.4,z+1.4],s===3?'white':s%2?'silver':'purple'));}}model('remembrance_flower',flower);
const stake=[box([3.2,8,3.2],[12.8,9.3,12.8],'dark'),box([4.0,9.3,4.0],[12,10.5,12],'gold'),box([5.6,10.4,5.6],[10.4,26,10.4],'purple'),box([6.6,10.8,5.2],[9.4,25.2,10.8],'light'),box([6.3,26,6.3],[9.7,28.6,9.7],'white'),box([7.2,28.6,7.2],[8.8,30.5,8.8],'light')];model('lightning_stake',stake);
// Static illusion retains the original full skin, origin at waist (place feet+1).
const illusion=[];const illParts=[[[4,16,4],[12,24,12],[0,0,8,8,8],[32,0,8,8,8],.4],[[4,4,6],[12,16,10],[16,16,8,12,4],[16,32,8,12,4],.2],[[0,4,6],[4,16,10],[40,16,4,12,4],[40,32,4,12,4],.2],[[12,4,6],[16,16,10],[32,48,4,12,4],[48,48,4,12,4],.2],[[4,-8,6],[8,4,10],[0,16,4,12,4],[0,32,4,12,4],.2],[[8,-8,6],[12,4,10],[16,48,4,12,4],[0,48,4,12,4],.2]];for(const[a,b,uv,over,inf]of illParts)illusion.push(sb(a,b,uv,0,uv[3]),sb(a,b,over,0,over[3],inf));model('illusion',illusion);

const zeros=[0,0,0],rad=d=>d*Math.PI/180;
function mul(a,b){const[x,y,z,w]=a,[X,Y,Z,W]=b;return[w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W,w*W-x*X-y*Y-z*Z];}
function q(e=zeros){const[x,y,z]=e.map(v=>rad(v)/2);return mul(mul([0,0,Math.sin(z),Math.cos(z)],[0,Math.sin(y),0,Math.cos(y)]),[Math.sin(x),0,0,Math.cos(x)]);}
const rot=(Q,v)=>mul(mul(Q,[...v,0]),[-Q[0],-Q[1],-Q[2],Q[3]]).slice(0,3),add=(a,b)=>a.map((x,i)=>x+b[i]),sub=(a,b)=>a.map((x,i)=>x-b[i]),times=(v,s)=>v.map(x=>x*s),lerp=(a,b,t)=>a.map((x,i)=>x+(b[i]-x)*t);
const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2],cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],unit=v=>times(v,1/Math.max(Math.hypot(...v),1e-9));
function aimDown(v){const len=Math.hypot(...v),n=times(v,1/Math.max(len,.0001));if(n[1]>.9999)return[1,0,0,0];const a=[-n[2],0,n[0],1-n[1]],m=Math.hypot(...a);return a.map(x=>x/m);}
// Rotation whose columns are the images of the authoring x/y/z axes (orthonormal, right-handed).
function basisQ(X,Y,Z){const m=[[X[0],Y[0],Z[0]],[X[1],Y[1],Z[1]],[X[2],Y[2],Z[2]]],tr=m[0][0]+m[1][1]+m[2][2];let s;
 if(tr>0){s=Math.sqrt(tr+1)*2;return[(m[2][1]-m[1][2])/s,(m[0][2]-m[2][0])/s,(m[1][0]-m[0][1])/s,s/4];}
 if(m[0][0]>m[1][1]&&m[0][0]>m[2][2]){s=Math.sqrt(1+m[0][0]-m[1][1]-m[2][2])*2;return[s/4,(m[0][1]+m[1][0])/s,(m[0][2]+m[2][0])/s,(m[2][1]-m[1][2])/s];}
 if(m[1][1]>m[2][2]){s=Math.sqrt(1+m[1][1]-m[0][0]-m[2][2])*2;return[(m[0][1]+m[1][0])/s,s/4,(m[1][2]+m[2][1])/s,(m[0][2]-m[2][0])/s];}
 s=Math.sqrt(1+m[2][2]-m[0][0]-m[1][1])*2;return[(m[0][2]+m[2][0])/s,(m[1][2]+m[2][1])/s,s/4,(m[1][0]-m[0][1])/s];}
// Authoring space (before the final z-mirror): +X = boss's left, +Y up, -Z forward. Item
// models appear x-flipped there, so model -X (the blade edge, the thumb) maps to the +X image.
// bq: blade tip (model +Y) and edge direction. hq: fingers (model -Y) and palm normal (+Z).
const bq=(tip,edge)=>{const T=unit(tip),E=unit(sub(edge,times(T,dot(edge,T))));return basisQ(E,T,cross(E,T));};
const hq=(fingers,palm)=>{const F=unit(fingers),P=unit(sub(palm,times(F,dot(palm,F)))),Y=times(F,-1);return basisQ(cross(Y,P),Y,P);};
// A level cut: theta 0 = tip forward, -90 = boss's right, +90 = boss's left; dir +1 travels
// toward the boss's left. chop: phi 0 = tip up, 90 = tip forward. The edge faces the travel.
const sweep=(theta,elev=0,dir=1)=>{const a=rad(theta),e=rad(elev);return bq([Math.sin(a)*Math.cos(e),Math.sin(e),-Math.cos(a)*Math.cos(e)],times([Math.cos(a),0,Math.sin(a)],dir));};
const chop=(phi,yaw=0)=>{const a=rad(phi),Y=q([0,yaw,0]);return bq(rot(Y,[0,Math.cos(a),-Math.sin(a)]),rot(Y,[0,-Math.sin(a),-Math.cos(a)]));};
const toQ=v=>v.length===4?v:q(v);
function slerp(a,b,t){let d=dot(a,b)+a[3]*b[3];if(d<0){b=b.map(x=>-x);d=-d;}if(d>.9995)return unit4(a.map((x,i)=>x+(b[i]-x)*t));const th=Math.acos(d),s=Math.sin(th);return a.map((x,i)=>(x*Math.sin((1-t)*th)+b[i]*Math.sin(t*th))/s);}
const unit4=v=>{const m=Math.hypot(...v);return v.map(x=>x/m);};
// Left-side keys mirror the right side: positions x -> -x, rotations [x,-y,-z,w] / euler [a,-b,-c].
const mx=v=>[-v[0],v[1],v[2]],mq=Q=>[Q[0],-Q[1],-Q[2],Q[3]];
const arm=(n,spec)=>Object.fromEntries(Object.entries(spec).map(([k,v])=>[n+'_'+k,v]));
const mirrorSpec=spec=>Object.fromEntries(Object.entries(spec).map(([k,v])=>[k,k==='hand'?(v.length===4?mq(v):[v[0],-v[1],-v[2]]):mx(v)]));
const pair=(r,l,spec,specL=mirrorSpec(spec))=>({...arm(r,spec),...arm(l,specL)});
const rear=(s,l)=>pair('rear_r','rear_l',s,l),rear2=(s,l)=>pair('rear2_r','rear2_l',s,l),cradle=(s,l)=>pair('support_r','main_l',s,l);
// One big lilac sword arm (main_r), two dull cradle hands under Raiden (support_r + main_l),
// and four smaller lilac arms fanned behind her shoulders (rear = upper pair, rear2 = lower).
const auxArms=['main_r','main_l','support_r','rear_r','rear_l','rear2_r','rear2_l'];
const auxSize={main_r:1.7,main_l:2.15,support_r:2.15,rear_r:.95,rear_l:.95,rear2_r:1.05,rear2_l:1.05};
// Segment thickness when it differs from the hand size: the cradle arms stay slimmer than their hands.
const auxThick={main_l:1.45,support_r:1.45};
const rotKeys=new Set(['giant_weapon',...auxArms.map(n=>n+'_hand')]);
const defaults={shift:[0,0,0],root:[0,0,0],torso:[0,0,0],head:[0,0,0],right_arm:[8,-8,-12],right_elbow:[16,0,0],left_arm:[5,0,9],left_elbow:[8,0,0],right_leg:[0,0,-2],right_knee:[0,0,0],left_leg:[0,0,2],left_knee:[0,0,0],weapon:[-18,0,0],ring:[0,0,0],form:[1],fade:[1],
 ...arm('main_r',{sh:[-.8,3.0,.75],el:[-1.95,3.55,.45],wr:[-2.1,2.3,-.75],hand:[0,0,-15]}),giant_weapon:bq([-.3,1,-.15],[.05,-.1,-1]),
 ...cradle({sh:[-.75,1.75,1.45],el:[-1.45,.3,1.45],wr:[-1.05,.45,.7],hand:hq([.55,.15,-.85],[0,1,0])}),
 ...rear({sh:[-.5,3.35,.95],el:[-1.55,3.75,1.0],wr:[-2.0,4.5,.85],hand:hq([-1,.85,0],[0,0,-1])}),
 ...rear2({sh:[-.55,2.6,1.0],el:[-1.6,2.45,1.1],wr:[-2.6,2.05,.9],hand:hq([-1,-.3,0],[0,0,-1])})};
const nd=o=>Object.fromEntries(Object.entries(o).map(([k,d])=>[k,add(defaults[k],d)])),back=(...ks)=>Object.fromEntries(ks.map(k=>[k,defaults[k]]));
const auxJoints=auxArms.flatMap(n=>['_sh','_el','_wr','_hand'].map(j=>n+j));
// Aux wrists drop and splay as the armour fails (k = 0..1).
const droop=k=>nd({rear_r_wr:[-.25*k,-1.15*k,.25*k],rear_l_wr:[.25*k,-1.2*k,.25*k],rear2_r_wr:[-.2*k,-.95*k,.2*k],rear2_l_wr:[.2*k,-.9*k,.2*k],support_r_wr:[-.1*k,-.22*k,.1*k],main_l_wr:[.1*k,-.22*k,.1*k]});
const key=(tick,pose)=>({tick,pose});
// Forward is authored -Z: a negative torso pitch bows the chest toward the knees.
// One knee rests low while the opposite foot carries the weight for the recovery.
const kneeling={shift:[0,-.25,-.025],root:[0,0,0],torso:[-34,0,3],head:[-20,0,-3],right_arm:[45,0,-14],right_elbow:[12,0,0],left_arm:[68,4,16],left_elbow:[34,0,0],right_leg:[52,0,-5],right_knee:[-104,0,0],left_leg:[5,0,5],left_knee:[-93,0,0],weapon:[-76,-10,15],form:[0],fade:[1]};
const upright=bq([-.15,1,-.28],[0,-.28,-1]),castPalm=hq([.12,1,-.1],[0,.1,-1]),pushPalm=hq([0,.75,-.65],[0,-.65,-.75]);
const clips=[
 {id:0,name:'idle',length:40,loop:true,keys:[key(0,{}),
  key(10,{...nd({rear_r_wr:[-.1,.12,-.04],rear_r_el:[-.05,.05,0],rear2_l_wr:[.1,.08,0],main_r_wr:[0,.04,0]}),rear_r_hand:hq([-.55,1,.05],[0,0,-1])}),
  key(20,{shift:[0,.035,0],head:[-2,0,0],left_arm:[7,0,11],ring:[0,0,4],...nd({support_r_wr:[0,.05,0],main_l_wr:[0,.05,0],rear_l_wr:[.1,.12,-.04],rear_l_el:[.05,.05,0],rear2_r_wr:[-.1,.08,0],rear_r_wr:[0,0,0],rear_r_el:[0,0,0],main_r_wr:[0,.05,0]}),rear_r_hand:defaults.rear_r_hand,rear_l_hand:mq(hq([-.55,1,.05],[0,0,-1]))}),
  key(30,{...nd({rear2_l_wr:[0,0,0],rear_l_wr:[.03,.04,0],rear_l_el:[0,0,0],rear2_r_wr:[0,0,0]}),rear_l_hand:defaults.rear_l_hand,ring:[0,0,2]}),
  key(40,back('shift','head','left_arm','ring','main_r_wr','rear_r_wr','rear_r_el','rear_l_wr','rear_l_el','rear2_r_wr','rear2_l_wr','support_r_wr','main_l_wr','rear_r_hand','rear_l_hand'))]},
 {id:1,name:'walk',length:24,loop:true,keys:[key(0,{right_leg:[23,0,-3],left_leg:[-23,0,3],right_arm:[-8,0,-12],left_arm:[22,0,10],weapon:[0,0,0]}),key(6,{shift:[0,.06,0],right_knee:[-20,0,0],left_knee:[-8,0,0]}),key(12,{right_leg:[-23,0,-3],left_leg:[23,0,3],right_arm:[20,0,-12],left_arm:[-14,0,10],right_knee:[0,0,0],left_knee:[0,0,0],shift:[0,0,0]}),key(18,{shift:[0,.06,0],right_knee:[-8,0,0],left_knee:[-20,0,0]}),key(24,{right_leg:[23,0,-3],left_leg:[-23,0,3],right_arm:[-8,0,-12],left_arm:[22,0,10],right_knee:[0,0,0],left_knee:[0,0,0],shift:[0,0,0]})]},
 {id:2,name:'slash_wind',length:18,keys:[key(0,{}),key(10,{torso:[-4,-36,-6],right_arm:[65,-35,-75],right_elbow:[32,0,0],left_arm:[18,10,33],left_elbow:[25,0,0],weapon:[-70,8,85],right_leg:[-8,0,-7],left_leg:[12,0,5],main_r_el:[-1.45,3.85,.7],main_r_wr:[-2.55,3.65,.15],giant_weapon:sweep(-120,25)}),key(18,{torso:[-5,-42,-8],right_arm:[70,-40,-80],right_elbow:[35,0,0],weapon:[-76,8,85],giant_weapon:sweep(-128,27)})]},
 {id:3,name:'slash_a',length:12,keys:[key(0,{torso:[-4,-40,-7],right_arm:[70,-40,-80],right_elbow:[35,0,0],weapon:[-76,8,85],main_r_el:[-1.45,3.85,.7],main_r_wr:[-2.55,3.65,.15],giant_weapon:sweep(-128,27)}),key(4,{torso:[10,28,8],right_arm:[88,55,-15],right_elbow:[8,0,0],weapon:[-20,85,90],left_arm:[-12,-10,40],main_r_wr:[.4,2.25,-2.25],main_r_el:[-1.1,3.3,-1.2],giant_weapon:sweep(0,-10)}),key(8,{torso:[8,40,12],right_arm:[70,74,10],weapon:[-15,85,90],main_r_wr:[1.45,1.75,-1.5],giant_weapon:sweep(80,-12)}),key(12,{torso:[3,20,5],right_arm:[35,35,-10],weapon:[-35,15,45],main_r_wr:[.8,2.15,-1.2],giant_weapon:bq([.4,1,-.3],[0,-.3,-1])})]},
 {id:4,name:'slash_b',length:12,keys:[key(0,{torso:[4,32,8],right_arm:[70,70,0],weapon:[-25,30,85],main_r_wr:[1.45,2,-1.5],main_r_el:[-.6,3.0,-1.2],giant_weapon:sweep(80,-5,-1)}),key(4,{torso:[8,-35,-7],right_arm:[95,-58,-44],weapon:[-55,-30,-78],left_arm:[-15,0,32],main_r_wr:[-2.3,2.3,-1.8],main_r_el:[-1.8,3.5,-1.2],giant_weapon:sweep(-75,-10,-1)}),key(12,{torso:[0,-15,-2],right_arm:[28,-20,-15],weapon:[-20,0,-30],main_r_wr:[-2.1,2.5,-1.0],main_r_el:defaults.main_r_el,giant_weapon:upright})]},
 {id:5,name:'thrust_wind',length:18,keys:[key(0,{}),key(12,{torso:[-4,-40,0],right_arm:[30,-42,-28],right_elbow:[68,0,0],left_arm:[36,10,25],left_elbow:[45,0,0],weapon:[-9,0,90],right_leg:[-16,0,-6],left_leg:[16,0,6],main_r_wr:[-1.65,2.6,.65],giant_weapon:bq([0,-.04,-1],[0,-1,0])}),key(18,{torso:[-6,-42,0]})]},
 {id:6,name:'thrust',length:14,keys:[key(0,{torso:[-4,-38,0],right_arm:[32,-40,-24],right_elbow:[60,0,0],weapon:[-4,0,90],main_r_wr:[-1.65,2.6,.65],giant_weapon:bq([0,-.04,-1],[0,-1,0])}),key(4,{shift:[0,0,-.18],torso:[18,10,0],right_arm:[90,4,-6],right_elbow:[2,0,0],weapon:[0,0,90],left_arm:[-22,-15,35],main_r_el:[-.9,2.85,-1.15],main_r_wr:[-.55,2.5,-2.35],giant_weapon:bq([0,-.08,-1],[0,-1,0]),...rear2({wr:[-1.9,2.35,-.4],hand:hq([0,.1,-1],[0,-1,0])})}),key(9,{shift:[0,0,-.1],torso:[8,0,0],right_arm:[78,2,-10]}),key(14,{shift:[0,0,0],torso:[0,0,0],right_arm:[24,0,-15],right_elbow:[10,0,0],weapon:[-10,0,0],...back('main_r_el','main_r_wr','rear2_r_wr','rear2_l_wr','rear2_r_hand','rear2_l_hand'),giant_weapon:upright})]},
 {id:7,name:'cast_wind',length:30,keys:[key(0,{}),key(12,{left_arm:[140,-15,35],left_elbow:[25,0,0],right_arm:[16,0,-16],head:[-13,-6,0],...rear({el:[-1.3,3.85,.5],wr:[-1.35,4.35,-.35],hand:castPalm}),...rear2({wr:[-2.55,3.35,.4],hand:hq([-.55,1,0],[0,0,-1])}),...cradle({wr:[-1.05,.78,.25]}),ring:[0,0,15]}),key(24,{left_arm:[157,-8,20],left_elbow:[12,0,0],head:[-18,0,0],...rear({el:[-1.3,3.9,.45],wr:[-1.3,4.45,-.4]}),...rear2({wr:[-2.6,3.45,.35]}),ring:[0,0,22]}),key(30,{left_arm:[160,-8,19]})]},
 {id:8,name:'cast',length:16,keys:[key(0,{left_arm:[160,-8,19],left_elbow:[12,0,0],...rear({el:[-1.3,3.9,.45],wr:[-1.3,4.45,-.4],hand:castPalm}),...rear2({wr:[-2.6,3.45,.35],hand:hq([-.55,1,0],[0,0,-1])}),...cradle({wr:[-1.05,.78,.25]})}),key(4,{torso:[10,0,0],left_arm:[92,-8,18],left_elbow:[2,0,0],...rear({el:[-1.35,3.45,-.05],wr:[-1.0,3.0,-1.2],hand:pushPalm}),...rear2({el:[-1.65,2.5,.05],wr:[-1.75,2.45,-1.35],hand:hq([.15,.15,-1],[0,-1,0])})}),key(10,{torso:[5,0,0],left_arm:[78,-8,22]}),key(16,{left_arm:[30,-5,17],left_elbow:[10,0,0],torso:[0,0,0],...back('rear_r_el','rear_l_el','rear_r_wr','rear_l_wr','rear_r_hand','rear_l_hand','rear2_r_el','rear2_l_el','rear2_r_wr','rear2_l_wr','rear2_r_hand','rear2_l_hand','support_r_wr','main_l_wr')})]},
 {id:9,name:'transform',length:70,keys:[key(0,{form:[0],torso:[18,0,0],head:[25,0,0],right_arm:[28,0,-12],left_arm:[28,0,12],right_elbow:[70,0,0],left_elbow:[70,0,0],...rear({wr:[-.75,3.0,.6]}),...rear2({wr:[-.95,2.35,.6]}),...cradle({wr:[-1.3,1.25,.65]}),main_r_wr:[-1.2,2.3,.3]}),key(16,{form:[.1],shift:[0,.1,0],torso:[-10,0,0],head:[-15,0,0],right_arm:[110,-10,-75],left_arm:[110,10,75],right_elbow:[25,0,0],left_elbow:[25,0,0],main_r_wr:[-1.2,2.3,.3],ring:[0,0,-30]}),key(38,{form:[.75],shift:[0,.15,0],right_arm:[42,0,-45],left_arm:[42,0,45],right_leg:[28,0,-10],left_leg:[28,0,10],right_knee:[-55,0,0],left_knee:[-55,0,0],main_r_wr:[-2.5,3.2,-.5],giant_weapon:bq([-.75,.65,-.1],[0,-.1,-1]),...rear({wr:[-2.1,5.0,.6],hand:hq([-.7,1,0],[0,0,-1])}),...rear2({wr:[-2.95,2.25,.6]}),...cradle({wr:[-1.15,.45,.05]}),ring:[0,0,10]}),key(56,{form:[1],shift:[0,0,0],torso:[0,0,0],head:[0,0,0],right_arm:[20,0,-16],left_arm:[20,0,16],right_elbow:[38,0,0],left_elbow:[38,0,0],...back(...auxJoints,'giant_weapon'),ring:[0,0,0]}),key(70,{})]},
 {id:10,name:'arm_sweep_wind',length:30,keys:[key(0,{}),key(18,{torso:[-5,-30,-6],main_r_el:[-1.4,3.9,.75],main_r_wr:[-2.85,4.15,.3],giant_weapon:sweep(-120,25),...arm('rear_r',{el:[-1.6,3.65,1.25],wr:[-2.2,4.15,1.3],hand:hq([-.7,.5,.5],[0,0,-1])}),...nd({rear2_r_wr:[.1,.25,.35]}),left_arm:[36,0,30],ring:[0,0,-10]}),key(30,{main_r_wr:[-2.95,4.25,.35],giant_weapon:sweep(-132,28)})]},
 {id:11,name:'arm_sweep',length:16,keys:[key(0,{torso:[-5,-30,-6],main_r_el:[-1.4,3.9,.75],main_r_wr:[-2.95,4.25,.35],giant_weapon:sweep(-132,28)}),key(4,{torso:[10,15,4],main_r_el:[-1.0,3.0,-1.6],main_r_wr:[0,2.5,-3.0],giant_weapon:sweep(0,-12),...arm('rear_r',{el:[-1.5,3.6,.4],wr:[-1.45,3.4,-.6],hand:hq([.2,.2,-1],[1,0,0])}),...rear2({el:[-1.75,2.4,.25],wr:[-1.6,2.1,-.9]},{wr:[2.75,2.75,.55]})}),key(8,{torso:[8,35,10],main_r_el:[-.3,2.8,-1.4],main_r_wr:[2.4,1.65,-1.3],giant_weapon:sweep(85,-15)}),key(16,{torso:[0,10,0],main_r_el:defaults.main_r_el,main_r_wr:[-1.5,2.3,-1.2],giant_weapon:upright,...back('rear_r_el','rear_r_wr','rear_r_hand','rear2_r_el','rear2_r_wr','rear2_l_wr')})]},
 {id:12,name:'clap_wind',length:32,keys:[key(0,{}),key(18,{...cradle({sh:[-1.0,2.35,1.2],el:[-2.3,1.55,.55],wr:[-2.6,2.65,-1.0],hand:hq([0,.75,-.65],[1,0,0])}),...rear({wr:[-1.0,4.15,.2]}),...nd({rear2_r_wr:[-.15,.35,0],rear2_l_wr:[.15,.35,0]}),main_r_wr:[-2.3,2.85,-.25],left_arm:[38,0,32],right_arm:[38,0,-32]}),key(32,{...cradle({wr:[-2.85,2.75,-1.1]})})]},
 {id:13,name:'clap',length:16,keys:[key(0,{...cradle({sh:[-1.0,2.35,1.2],el:[-2.3,1.55,.55],wr:[-2.85,2.75,-1.1],hand:hq([0,.75,-.65],[1,0,0])}),main_r_wr:[-2.3,2.85,-.25]}),key(4,{torso:[12,0,0],...cradle({sh:[-.9,2.2,1.1],el:[-1.75,1.55,-.6],wr:[-.33,2.1,-2.2],hand:hq([0,.55,-.85],[1,0,0])}),right_arm:[74,0,-12],left_arm:[74,0,12],...nd({rear2_r_wr:[.2,.1,-.4],rear2_l_wr:[-.2,.1,-.4]})}),key(8,{...cradle({wr:[-.37,2.1,-2.2]})}),key(16,{torso:[0,0,0],...cradle({sh:defaults.support_r_sh,el:[-1.6,.6,1.0],wr:[-1.15,.85,.1],hand:defaults.support_r_hand}),...back('main_r_wr','rear_r_wr','rear_l_wr','rear2_r_wr','rear2_l_wr')})]},
 {id:14,name:'slam_wind',length:30,keys:[key(0,{}),key(18,{torso:[-15,0,0],head:[-18,0,0],main_l_sh:[1.0,2.3,.9],main_l_el:[2.1,3.0,.6],main_l_wr:[1.5,4.7,-.35],main_l_hand:hq([.1,1,.1],[0,0,-1]),rear_r_wr:[-1.1,4.2,-.2],rear_l_wr:[1.25,4.1,-.2],left_arm:[142,0,25],right_arm:[110,0,-25]}),key(30,{main_l_wr:[1.45,4.95,-.4]})]},
 {id:15,name:'slam',length:20,keys:[key(0,{main_l_sh:[1.0,2.3,.9],main_l_el:[2.1,3.0,.6],main_l_wr:[1.45,4.95,-.4],main_l_hand:hq([.1,1,.1],[0,0,-1]),torso:[-15,0,0]}),key(5,{torso:[30,0,0],head:[12,0,0],main_l_el:[1.9,1.6,-.7],main_l_wr:[.95,.34,-2.0],main_l_hand:hq([0,-.05,-1],[0,-1,0]),...rear({el:[-1.5,3.2,.1],wr:[-1.35,2.4,-1.05],hand:hq([0,-.3,-1],[0,-1,.3])}),left_arm:[95,0,18],right_arm:[84,0,-22]}),key(10,{main_l_wr:[.95,.34,-2.0]}),key(20,{torso:[5,0,0],...back('main_l_sh','main_l_el','main_l_wr','main_l_hand','rear_r_el','rear_l_el','rear_r_wr','rear_l_wr','rear_r_hand','rear_l_hand'),left_arm:[30,0,20]})]},
 {id:16,name:'judgment_wind',length:64,keys:[key(0,{}),key(18,{main_r_el:[-1.6,3.9,.35],main_r_wr:[-.8,4.75,-.35],giant_weapon:chop(-10),...cradle({wr:[-1.05,.82,.2]}),...rear({el:[-1.25,3.7,.2],wr:[-.85,3.5,-.8],hand:castPalm}),...rear2({wr:[-2.65,3.15,.55],hand:hq([-.5,1,0],[0,0,-1])}),right_arm:[150,0,-14],left_arm:[130,0,15],head:[-20,0,0],ring:[0,0,-15]}),key(42,{main_r_wr:[-.3,5.1,-.25],giant_weapon:chop(-25),...rear({el:[-1.1,3.85,.25],wr:[-.6,4.0,-.6]}),right_arm:[170,0,-10],left_arm:[152,0,10],ring:[0,0,20]}),key(64,{main_r_wr:[-.28,5.25,-.25],giant_weapon:chop(-30),ring:[0,0,40]})]},
 {id:17,name:'judgment',length:26,keys:[key(0,{main_r_el:[-1.6,3.9,.35],main_r_wr:[-.28,5.25,-.25],giant_weapon:chop(-30),head:[-20,0,0],right_arm:[170,0,-10],left_arm:[152,0,10]}),key(6,{torso:[32,0,0],head:[15,0,0],main_r_el:[-1.05,2.8,-1.3],main_r_wr:[-.25,1.75,-2.35],giant_weapon:chop(110),...rear({el:[-1.6,3.3,.15],wr:[-1.55,2.55,-.95],hand:hq([0,-.4,-1],[0,-1,.4])}),...rear2({el:[-1.9,2.2,.45],wr:[-2.2,1.6,-.6],hand:hq([-.3,-.2,-1],[0,-1,0])}),right_arm:[120,0,-10],left_arm:[85,0,20]}),key(13,{torso:[28,0,0],main_r_wr:[-.25,1.65,-2.3],giant_weapon:chop(113)}),key(26,{torso:[8,0,0],main_r_el:defaults.main_r_el,main_r_wr:[-1.1,2.2,-1.0],giant_weapon:upright,right_arm:[50,0,-15],left_arm:[35,0,20],...back('rear_r_el','rear_l_el','rear_r_wr','rear_l_wr','rear_r_hand','rear_l_hand','rear2_r_el','rear2_l_el','rear2_r_wr','rear2_l_wr','rear2_r_hand','rear2_l_hand','support_r_wr','main_l_wr')})]},
 {id:18,name:'stagger',length:30,keys:[key(0,{}),key(4,{torso:[-23,0,-8],head:[-18,0,8],right_arm:[-15,10,-35],left_arm:[-15,-10,35],main_r_wr:[-2.35,2.3,.2],...droop(.3)}),key(13,{torso:[25,0,3],head:[20,0,0],right_arm:[25,0,-12],left_arm:[25,0,12],right_knee:[-30,0,0],left_knee:[-30,0,0],shift:[0,-.15,0]}),key(30,{torso:[20,0,0],head:[18,0,0],shift:[0,-.18,0]})]},
 {id:19,name:'death',length:48,keys:[key(0,{form:[1]}),key(4,{shift:[0,.03,.03],torso:[18,-3,-7],head:[15,0,8],right_arm:[-8,0,-30],left_arm:[-12,0,34],right_elbow:[20,0,0],left_elbow:[16,0,0],main_r_wr:[-2.6,2.1,.25],...droop(.25),form:[1]}),key(12,{shift:[0,-.22,-.025],torso:[-18,0,5],head:[-15,0,-4],right_arm:[30,0,-18],left_arm:[55,0,22],right_leg:[48,0,-7],right_knee:[-100,0,0],left_leg:[20,0,7],left_knee:[-90,0,0],main_r_wr:[-2.4,1.0,-.2],...droop(.7),giant_weapon:bq([-.25,-.55,-.8],[0,-.8,.55]),form:[.70]}),key(22,{...kneeling,shift:[0,-.27,-.04],torso:[-55,0,6],head:[-27,0,-4],right_arm:[44,0,-20],right_elbow:[18,0,0],left_arm:[74,0,24],left_elbow:[18,0,0],...droop(1),form:[.16]}),key(30,{shift:[0,-.32,-.07],torso:[-72,-6,8],head:[-24,0,-5],right_arm:[62,0,-24],right_elbow:[10,0,0],left_arm:[78,0,22],left_elbow:[8,0,0],form:[0],fade:[1]}),key(38,{shift:[0,-.32,-.07],torso:[-75,-6,8],fade:[.94]}),key(44,{shift:[0,-.15,-.07],fade:[.44]}),key(48,{shift:[0,.15,-.07],fade:[0]})]},
 {id:20,name:'spin',length:24,loop:true,keys:[key(0,{root:[0,0,0],right_arm:[80,0,-82],weapon:[-70,0,90],left_arm:[40,0,60],giant_weapon:bq([-.26,-.05,-.97],[-.97,0,.26]),main_r_wr:[-2.8,2.6,-.4]}),key(6,{root:[0,90,0],main_r_wr:[-2.6,2.7,-.5]}),key(12,{root:[0,180,0],main_r_wr:[-2.8,2.6,-.4]}),key(18,{root:[0,270,0],main_r_wr:[-2.6,2.7,-.5]}),key(24,{root:[0,360,0],main_r_wr:[-2.8,2.6,-.4]})]},
 {id:21,name:'dash',length:16,loop:true,keys:[key(0,{shift:[0,-.08,0],torso:[30,0,0],head:[-15,0,0],right_arm:[-38,-8,-16],left_arm:[-30,8,20],right_elbow:[10,0,0],left_elbow:[10,0,0],right_leg:[40,0,-5],left_leg:[-38,0,5],weapon:[-35,0,-20],main_r_wr:[-2,2.2,.8],giant_weapon:bq([-.35,-.4,.85],[.1,.3,-1]),...nd({rear_r_wr:[0,-.2,.45],rear_l_wr:[0,-.2,.45],rear2_r_wr:[.1,-.1,.5],rear2_l_wr:[-.1,-.1,.5]})}),key(8,{right_leg:[-38,0,-5],left_leg:[40,0,5],right_knee:[-30,0,0],left_knee:[-5,0,0]}),key(16,{right_leg:[40,0,-5],left_leg:[-38,0,5],right_knee:[-5,0,0],left_knee:[-30,0,0]})]},
 {id:22,name:'exhausted',length:60,loop:true,keys:[key(0,kneeling),key(30,{shift:[0,-.23,-.025],torso:[-31,0,3],head:[-17,0,-3],left_arm:[66,4,16]}),key(60,kneeling)]},
 {id:23,name:'collapse',length:46,keys:[key(0,{form:[1]}),key(4,{shift:[0,.025,.02],torso:[20,-5,-7],head:[16,0,8],right_arm:[-10,0,-28],left_arm:[-8,0,32],right_elbow:[20,0,0],left_elbow:[16,0,0],main_r_wr:[-2.5,2.5,.2],...droop(.2),form:[1]}),key(11,{shift:[0,-.06,-.005],torso:[-10,0,5],head:[-5,0,-4],right_arm:[26,0,-18],left_arm:[40,0,22],right_leg:[28,0,-6],left_leg:[24,0,6],right_knee:[-55,0,0],left_knee:[-58,0,0],main_r_wr:[-2.3,1.8,-.15],...droop(.6),giant_weapon:bq([-.3,-.5,-.8],[0,-.8,.5]),form:[.88]}),key(20,{...kneeling,shift:[0,-.13,-.015],torso:[-42,0,5],head:[-25,0,-4],right_arm:[54,0,-16],left_arm:[72,4,20],...droop(1),form:[.30]}),key(30,{...kneeling,shift:[0,-.27,-.035],torso:[-43,0,4],head:[-24,0,-4],form:[0]}),key(38,{...kneeling,shift:[0,-.245,-.025],torso:[-32,0,3]}),key(46,kneeling)]},
 {id:24,name:'recover',length:28,keys:[key(0,kneeling),key(6,{shift:[0,-.26,-.02],torso:[-48,0,1],head:[-8,0,0],left_arm:[76,4,18],left_elbow:[18,0,0],right_arm:[43,0,-14],right_leg:[56,0,-5],right_knee:[-106,0,0],left_knee:[-98,0,0]}),key(14,{shift:[0,-.12,-.01],torso:[-25,0,0],head:[-3,0,0],right_leg:[28,0,-4],right_knee:[-55,0,0],left_leg:[12,0,4],left_knee:[-50,0,0],right_arm:[20,0,-12],left_arm:[46,4,15],left_elbow:[15,0,0]}),key(22,{shift:[0,0,0],torso:[-6,0,0],head:[0,0,0],right_leg:[5,0,-2],right_knee:[-10,0,0],left_leg:[5,0,2],left_knee:[-10,0,0],right_arm:[8,-8,-12],right_elbow:[16,0,0],left_arm:[10,0,10],left_elbow:[8,0,0]}),key(28,{shift:[0,0,0],torso:[0,0,0],head:[0,0,0],right_leg:[0,0,-2],right_knee:[0,0,0],left_leg:[0,0,2],left_knee:[0,0,0],left_arm:[5,0,9],form:[0]})]}
];
// Attacks accelerate into contact, hold only a brief impact beat, then recover.
// Controller contract: contact key 2 (+1 interpolation), heavy contact key 3 (+1).
const retime={
 1:[0,4,9,13,18],2:[0,3,5],3:[0,2,4,7],4:[0,2,7],
 5:[0,3,5],6:[0,2,5,9],7:[0,3,5,6],8:[0,2,5,9],
 9:[0,10,25,38,46],10:[0,4,6],11:[0,2,4,9],12:[0,5,8],
 13:[0,2,4,9],14:[0,5,8],15:[0,3,5,12],16:[0,5,8,9],
 17:[0,3,6,15],20:[0,3,6,9,12],21:[0,5,10]
};
for(const c of clips)if(retime[c.id]){if(retime[c.id].length!==c.keys.length)throw new Error(`clip ${c.name}: ${c.keys.length} keys for ${retime[c.id].length} retimed ticks`);c.keys.forEach((k,i)=>k.tick=retime[c.id][i]);c.length=c.keys.at(-1).tick;}
const hitTick=new Map([[3,2],[4,2],[6,2],[8,2],[11,2],[13,2],[15,3],[17,3]]);
const windIds=new Set([2,5,7,10,12,14,16]);
const fxNames=['weapon_fx','weapon_trail_1','weapon_trail_2','weapon_trail_3','giant_fx','giant_trail_1','giant_trail_2','giant_trail_3'];
// Palm lightning follows these hands; during the clap the sword hand's charge moves to the
// right cradle hand, which claps together with the left one (main_l).
const palmParts={palm_main_r:'main_r_hand',palm_main_l:'main_l_hand',palm_rear_r:'rear_r_hand',palm_rear_l:'rear_l_hand'};
const palmHand=(n,anim)=>n==='palm_main_r'&&[12,13].includes(anim)?'support_r_hand':palmParts[n];
const powerFxNames=[...Object.keys(palmParts),'palm_skin','chakra_fx'];
const pnames=[...Object.keys(bodySpecs),'weapon','armor','crown','ribbon_r','ribbon_l','chakra',...auxArms.flatMap(n=>[n+'_upper',n+'_forearm',n+'_hand']),'giant_weapon',...fxNames,...powerFxNames];
// How much of the Shadowlord form shows (before the death fade).
function armorAmount(p,phase,anim){let armor=phase===2?1:phase===1?p.form[0]:0;if(anim===23&&phase===3)armor=p.form[0];if(anim===19&&(phase===1||phase===2))armor=p.form[0];return armor;}
function posed(p,phase,anim){
 const form=armorAmount(p,phase,anim)*p.fade[0],bodyScale=(1.20+.38*form)*p.fade[0],lift=1.05*form,hip=add([0,.75,0],p.shift),root=q(p.root),body=q(p.torso),top=add(hip,rot(body,[0,.75,0])),o={body:{t:top,q:body},head:{t:top,q:mul(body,q(p.head))}};
 for(const[side,sign]of[['right',-1],['left',1]]){const sh=add(hip,rot(body,[sign*.375,.625,0])),arm=mul(body,q(p[side+'_arm'])),el=add(sh,rot(arm,[0,-.25,0])),fore=mul(arm,q(p[side+'_elbow'])),leg=q(p[side+'_leg']),pelvis=add(hip,[sign*.125,0,0]);o[side+'_arm']={t:sh,q:arm};o[side+'_forearm']={t:el,q:fore};o[side+'_leg']={t:pelvis,q:leg};o[side+'_shin']={t:add(pelvis,rot(leg,[0,-.375,0])),q:mul(leg,q(p[side+'_knee']))};if(side==='right'){
   // Blade +Y must point into the attack. Solve its final orientation in body
   // space while retaining the animated hand pivot; a hanging arm's -Y axis
   // must never silently reverse a spear thrust or turn a cut into a back strike.
   // slash_wind/slash_a and spin travel toward the boss's right, so their blade is rolled
   // half a turn about its own axis: the white edge (model -X) leads every cut.
   let blade=q([-15,0,-15]);
   if([2,3,4].includes(anim))blade=q([-90,p.torso[1]*1.15,0]);
   if([2,3].includes(anim))blade=mul(blade,q([0,180,0]));
   if([5,6].includes(anim))blade=q([-90,p.torso[1]*.35,0]);
   if(anim===20)blade=mul(q([-90,-70,0]),q([0,180,0]));
   if(anim===21)blade=q([-18,0,-28]);
   if([19,22,23].includes(anim))blade=q([-80,-10,15]);
   if(anim===24){const u=Math.max(0,Math.min(1,-p.torso[0]/34));blade=q([-15-65*u,-10*u,-15+30*u]);}
   o.weapon={t:add(el,rot(fore,[0,-.31,0])),q:blade,s:[1.12,1.12,1.12]};
 }}
 o.armor={t:top,q:body,s:[form,form,form]};o.crown={...o.head,s:[form,form,form]};o.ribbon_r={t:add(top,rot(body,[-.2,-.38,.25])),q:mul(body,q([12,0,-8]))};o.ribbon_l={t:add(top,rot(body,[.2,-.38,.25])),q:mul(body,q([8,0,8]))};
 for(const v of Object.values(o)){v.t=add(hip,rot(root,sub(v.t,hip)));v.q=mul(root,v.q);v.t=add(times(v.t,bodyScale),[0,lift,0]);v.s=times(v.s||[1,1,1],bodyScale);}
 if(form>.01)o.weapon.s=[0,0,0];
 for(const n of auxArms){const sh=p[n+'_sh'],el=p[n+'_el'],wr=p[n+'_wr'];for(const[part,a,b,base]of[['upper',sh,el,.75],['forearm',el,wr,.875]]){const delta=sub(b,a);const th=(auxThick[n]||auxSize[n])*form;o[n+'_'+part]={t:a,q:aimDown(delta),s:[th,Math.hypot(...delta)/base*form,th]};}o[n+'_hand']={t:wr,q:p[n+'_hand'],s:Array(3).fill(auxSize[n]*form)};}
 // The big lilac fist closes around the katana grip: thumb toward the tsuba (tip), knuckles
 // continuing the forearm, the grip passing through the curled fingers.
 const gq=p.giant_weapon,tip=rot(gq,[0,1,0]),fore=sub(p.main_r_wr,p.main_r_el);let F=sub(fore,times(tip,dot(fore,tip)));if(Math.hypot(...F)<.2)F=rot(gq,[1,0,0]);F=unit(F);
 const palm=cross(tip,times(F,-1)),fs=auxSize.main_r/16;o.main_r_hand.q=basisQ(tip,times(F,-1),palm);
 o.giant_weapon={t:add(p.main_r_wr,add(add(times(F,6.2*fs),times(palm,.75*fs)),times(tip,2.6/16*2.15))),q:gq,s:Array(3).fill(2.15*form)};
 o.chakra={t:[0,3.28,1.05],q:q(p.ring),s:Array(3).fill(1.65*form)};
 for(const n of[...auxArms.flatMap(n=>[n+'_upper',n+'_forearm',n+'_hand']),'chakra','giant_weapon']){const v=o[n];v.t=add([0,2,0],rot(root,sub(v.t,[0,2,0])));v.q=mul(root,v.q);}
 for(const v of Object.values(o)){v.t=[v.t[0],v.t[1],-v.t[2]];v.q=[-v.q[0],-v.q[1],v.q[2],v.q[3]];}
 return o;
}
const f=x=>(Math.abs(x)<.0000005?0:x).toFixed(6)+'f',arr=a=>'['+a.map(f).join(',')+']';
const nbt=v=>`{translation:${arr(v.t)},left_rotation:${arr(v.q)},scale:${arr(v.s||[1,1,1])},right_rotation:[0f,0f,0f,1f]}`;
const handModel={main_r:'puppet_hand_closed',main_l:'support_hand_l',support_r:'support_hand_r',rear_r:'puppet_hand_open',rear_l:'puppet_hand_open_l',rear2_r:'puppet_hand_claw',rear2_l:'puppet_hand_claw_l'};
function modelFor(n,anim=0){
 if(n==='chakra_fx')return'fx_weapon/chakra_0';
 if(n.startsWith('palm_'))return palmModel(n,anim,false,0);
 if(fxNames.includes(n)){const kind=n.startsWith('weapon')&&[5,6].includes(anim)?'polearm':'katana';return'fx_weapon/'+kind+(n.includes('trail')?'_trail':'')+'_0';}
 if(n==='weapon')return[5,6].includes(anim)?'polearm':'katana';if(n==='giant_weapon')return'giant_katana';
 const aux=auxArms.find(a=>n.startsWith(a+'_'));if(aux){const part=n.slice(aux.length+1),cradleArm=aux==='main_l'||aux==='support_r';return part==='hand'?handModel[aux]:(cradleArm?'support_':'puppet_')+part;}
 if(n.startsWith('ribbon_'))return'ribbon';return n;
}
function palmModel(n,anim,release,variant){
 const closed=n==='palm_main_r'&&![12,13].includes(anim);
 return`fx_weapon/palm_${closed?'closed':'open'}_${release==='focus'?'focus':release?'release':'charge'}_${variant}`;
}
function sample(clip,t){let prev=structuredClone(defaults);const ks=clip.keys.map(k=>{prev={...prev,...k.pose};return{tick:k.tick,p:structuredClone(prev)};});let a=ks[0],b=a;for(const k of ks){if(k.tick<=t)a=k;else{b=k;break;}b=a;}const u=a.tick===b.tick?0:(t-a.tick)/(b.tick-a.tick),contact=hitTick.get(clip.id),smooth=contact!==undefined&&b.tick===contact?u*u:contact!==undefined&&a.tick>=contact?1-(1-u)*(1-u):u*u*(3-2*u);return Object.fromEntries(Object.keys(defaults).map(k=>[k,rotKeys.has(k)?slerp(toQ(a.p[k]),toQ(b.p[k]),smooth):lerp(a.p[k],b.p[k],smooth)]));}
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
 for(const n of Object.keys(palmParts)){
  const v=structuredClone(o[palmHand(n,clip.id)]),rear=n.includes('rear'),allow=n==='palm_main_r'?[12,13,16,17].includes(clip.id):handCast;
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
// Raiden's own skin and ribbons swap to their dull tinted copies while the armour carries
// her: once per clip/phase change (select) and on the tick the armour crosses half form.
const skinParts=[...Object.keys(bodySpecs),'ribbon_r','ribbon_l'];
for(const dull of[false,true])fn('skin_'+(dull?'dull':'normal'),[`# Raiden ${dull?'darkens inside the Shadowlord armour':'regains her own colours'}; item identity only.`,...skinParts.map(n=>`data modify entity @e[tag=rlk_rd_${n},limit=1] item.components."minecraft:item_model" set value "rlk:raiden/${(n.startsWith('ribbon_')?'ribbon':n)+(dull?'_dull':'')}"`)]);
const dullAt=(c,phase,t)=>{const p=sample(c,t);return armorAmount(p,phase,c.id)*p.fade[0]>=.5;};
// The reference's final disappearance becomes six distinct translucent display
// splinters lifting away from the collapsing body. Nothing persists after cleanup.
// Each splinter is a painted crystal (rig_shard: white ridge, lavender body, violet rim) on two
// crossed cards, two small side slivers and a star glint at its tip; constant item tints
// separate the violet, pale and lavender splinters.
for(let i=0;i<3;i++)fxModel('death_shard_'+i,[card('rig_shard','z',8,['x',6,10],['y',12.8,2.3]),card('rig_shard','x',8,['z',6,10],['y',12.8,2.3],{uv:[16,0,0,16]}),
 card('rig_shard','z',8.35,['x',6.0,7.5],['y',8.9,4.6],{rot:['z',22.5]}),card('rig_shard','z',7.65,['x',8.6,10.1],['y',11.5,7.4],{rot:['z',-22.5]}),
 card('glint','z',7.4,['x',6.5,9.5],['y',14.1,11.1]),card('glint','x',8.6,['z',6.5,9.5],['y',14.1,11.1])],[0xB894FF,null,0xDCCBFF][i]);
const deathParts=Array.from({length:6},(_,i)=>`rlk_rd_death_${i}`);
fn('death_fx_spawn',['kill @e[tag=rlk_rd_death_fx]',...deathParts.map((n,i)=>`summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_death_fx","${n}"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",brightness:{block:15,sky:15},interpolation_duration:1,teleport_duration:0,view_range:3f,width:0f,height:0f,shadow_radius:0f,transformation:{translation:[0f,0.8f,0f],left_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f],right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/death_shard_${i%3}"}}}`)]);
for(let t=0;t<=48;t++){
 const u=Math.max(0,Math.min(1,(t-18)/30)),envelope=Math.sin(u*Math.PI),lines=[];
 for(let i=0;i<6;i++){const a=i*Math.PI/3+.13,spread=.25+u*(1.0+(i%2)*.55),height=.55+u*(2.7+(i%3)*.4),scale=(.5+(i%2)*.25)*envelope,v={t:[Math.cos(a)*spread,height,Math.sin(a)*spread],q:q([12+u*60,a*180/Math.PI+u*80,20*Math.sin(i+u*3)]),s:[scale,scale*(1.3+u),scale]};lines.push(`data merge entity @e[tag=${deathParts[i]},limit=1] {interpolation_duration:1,start_interpolation:0,transformation:{translation:${arr(v.t)},left_rotation:${arr(v.q)},scale:${arr(v.s)},right_rotation:[0f,1f,0f,0f]}}`);}
 fn('death_fx/'+t,lines);
}
fn('death_fx_tick',Array.from({length:49},(_,t)=>`execute if score @s rdRigT matches ${t} run function rlk:boss/raiden/rig/death_fx/${t}`));
for(const c of clips){
 const dispatch=[],skin0=[];for(const phase of[0,1,2,3]){const phaseName=phase===0?'normal':phase===1?'forming':phase===2?'armored':'exhausted';skin0.push(`execute if score @s rdPhase matches ${phase} run function rlk:boss/raiden/rig/skin_${dullAt(c,phase,0)?'dull':'normal'}`);for(let t=0;t<=c.length;t++){const lines=poseLines(withLightning(c,t,phase));if(t>0&&dullAt(c,phase,t)!==dullAt(c,phase,t-1))lines.push(`function rlk:boss/raiden/rig/skin_${dullAt(c,phase,t)?'dull':'normal'}`);fn(`poses/${phaseName}/${c.name}/${t}`,lines);dispatch.push(`execute if score @s rdPhase matches ${phase} if score @s rdRigT matches ${t} run function rlk:boss/raiden/rig/poses/${phaseName}/${c.name}/${t}`);}}
 fn('clip/'+c.name,[...(!c.loop?[`execute if score @s rdRigT matches ${c.length+1}.. run return 0`]:[`execute if score @s rdRigT matches ${c.length+1}.. run scoreboard players set @s rdRigT 0`]),...dispatch,...(c.id===19?['execute if score @s rdRigT matches 0 run function rlk:boss/raiden/rig/death_fx_spawn','function rlk:boss/raiden/rig/death_fx_tick']:[])]);
 fn('select/'+c.name,['# Only item identity changes here; the next pose interpolates from the current pose.',...skin0,...['weapon',...fxNames,...powerFxNames].map(n=>`data modify entity @e[tag=rlk_rd_${n},limit=1] item.components."minecraft:item_model" set value "rlk:raiden/${modelFor(n,c.id)}"`)]);
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
// A remote dull support hand makes the targeted ground slam visibly reach its marked circle.
// Its entity origin is the captured ground point, never the moving boss/player.
// Advance it after boss AI each world tick, in the same order as hazard ages:
// summon tick = age 0; start the fast fall 3 ticks before contact and land at
// SLAM_CONTACT = the pattern 13 hazard tell (build_raiden_encounter.py). Palm down, fingers toward +Z, palm centred on the origin.
// It deliberately does not carry rlk_raiden_part, so rig/tick cannot teleport it.
const SLAM_CONTACT=12,slamS=4.6,slamPose=(y,s)=>`{translation:[0f,${f(y)},${f(-.3875*s)}],left_rotation:[-0.7071068f,0f,0f,0.7071068f],scale:[${f(s)},${f(s)},${f(s)}],right_rotation:[0f,0f,0f,1f]}`;
const slamAt=(age,dur,y,s)=>`execute if score @s rdRigT matches ${age} run data merge entity @s {interpolation_duration:${dur},start_interpolation:0,transformation:${slamPose(y,s)}}`;
fn('target_slam_spawn',[
 '# Called positioned at the fixed target ground point. This helper does no damage.',
 'tag @e[tag=rlk_rd_slam_new] remove rlk_rd_slam_new',
 `summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_slam_hand","rlk_rd_slam_new"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:0,view_range:2.5f,width:16f,height:20f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:${slamPose(7,.01)},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/support_hand_l"}}}`,
 'scoreboard players set @e[tag=rlk_rd_slam_new,limit=1] rdRigT -1',
 'tag @e[tag=rlk_rd_slam_new] remove rlk_rd_slam_new'
]);
fn('target_slam_tick',[
 '# @s = one floating hand, at its fixed ground origin. rdRigT is its age.',
 'execute unless entity @e[tag=rlk_raiden,scores={rdPhase=2,rdPat=13},limit=1] run return run kill @s',
 'scoreboard players add @s rdRigT 1',
 slamAt(1,4,7,slamS),slamAt(SLAM_CONTACT-7,4,7.45,slamS),slamAt(SLAM_CONTACT-3,3,.2*slamS,slamS),slamAt(SLAM_CONTACT+1,2,.2*slamS+.45,slamS),slamAt(SLAM_CONTACT+5,6,.2*slamS+.9,0),
 `execute if score @s rdRigT matches ${SLAM_CONTACT+14}.. run kill @s`
]);
const initial=withLightning(clips[0],0,0);
fn('spawn',['function rlk:boss/raiden/rig/cleanup',...pnames.map(n=>`summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_part","rlk_raiden_aux","rlk_rd_${n}"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:2.5f,width:16f,height:16f,shadow_radius:0f,brightness:{block:${Object.hasOwn(bodySpecs,n)?12:15},sky:15},transformation:${nbt(initial[n])},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/${modelFor(n)}"}}}`),'scoreboard players set @s rdRigA -1','scoreboard players set @s rdRigP -1','scoreboard players set @s rdRigT 0','scoreboard players set @s rdRigHit 0','execute rotated as @s rotated ~ 0 run tp @e[tag=rlk_raiden_part] ~ ~ ~ ~ 0']);
fn('changed',['scoreboard players set @s rdRigT 0','scoreboard players operation @s rdRigA = @s rdAnim','scoreboard players operation @s rdRigP = @s rdPhase',...clips.map(c=>`execute if score @s rdAnim matches ${c.id} run function rlk:boss/raiden/rig/select/${c.name}`)]);
fn('tick',['# @s = unique real boss. Parts inherit body yaw but never pitch.','execute unless entity @e[tag=rlk_raiden_part,limit=1] run function rlk:boss/raiden/rig/spawn','execute rotated as @s rotated ~ 0 run tp @e[tag=rlk_raiden_part] ~ ~ ~ ~ 0','execute unless score @s rdAnim = @s rdRigA run function rlk:boss/raiden/rig/changed','execute unless score @s rdPhase = @s rdRigP run function rlk:boss/raiden/rig/changed',...clips.map(c=>`execute if score @s rdAnim matches ${c.id} run function rlk:boss/raiden/rig/clip/${c.name}`),'function rlk:boss/raiden/rig/lightning_tick','execute if score @s rdRigHit matches 1 run execute as @e[tag=rlk_raiden_part] run data merge entity @s {Glowing:0b}','execute if score @s rdRigHit matches 1.. run scoreboard players remove @s rdRigHit 1','scoreboard players add @s rdRigT 1']);
json(path.join(here,'raiden_rig_manifest.json'),{parts:pnames.length,phase:{0:'normal',1:'transforming',2:'Baleful Shadowlord',3:'exhausted'},armSilhouette:'two skin arms; one big lilac sword arm (main_r) gripping the pale violet giant katana; four smaller lilac auxiliary arms fanned behind the shoulders (rear_* upper pair, rear2_* lower pair); two dull bronze-grey support hands (support_r, main_l) cradling a dull-tinted Raiden from below',palette:{armour:'arm_lilac plates, arm_shade sides, arm_deep joints, gold_dull trims, arm_tomoe/gold_dull tomoe discs',katana:'blade_pale body, blade_edge cutting edge on model -X, blade_core fuller and spine on +X, grip_dark grip, gold_dull tsuba/habaki/wraps',support:'hand_dull, hand_dull_dark, nail_glow nails and seams',raiden:`skin/ribbon *_dull copies tinted #${DULL_TINT.toString(16).toUpperCase()} while the armour is at least half formed`},blades:'Every blade frame is authored as (tip, edge); the edge (model -X) faces the direction of travel in all cuts. Rotation keys (giant_weapon, *_hand) are slerped.',lightning:{weaponDisplays:8,palmDisplays:5,chakraDisplays:1,materials:'painted gradient sprites (rlk:raiden/fxg/*: rig_katana, blade, rim_crackle, blade_trail, rig_palm, chakra, orb_core, rig_crown, arc, vbolt, charge_spark) on flat crossed cards',hands:'exact hand pivot/rotation/scale; charge, inward focus, contact release; smaller rear hands never emit large release crowns; the clap charge sits on the two support hands',chakra:'sparse outer-rim forks; idle intermittent, charged attacks sustained; empty centre preserves face visibility'},targetSlam:`dull support hand, palm down; grows from age 1, falls from age ${SLAM_CONTACT-3}, contacts the ground at hazard age ${SLAM_CONTACT}, removed at age ${SLAM_CONTACT+14}`,clips:clips.map(({id,name,length,loop})=>({id,name,length,loop:!!loop})),integration:'Call rig/init from load, rig/spawn and rig/tick as the real boss at its feet. rdAnim selects a state; private rdRigT resets on rdAnim/rdPhase changes. rig/select/<clip> also applies rig/skin_dull or rig/skin_normal for the current rdPhase. rig/flash is optional body-hit feedback. rig/cleanup deletes all parts. Supplied skin remains byte-identical.'});
console.log(`Built Raiden: ${pnames.length} animated parts (big sword arm, four auxiliary arms, two cradle hands), ${clips.length} motion states, four phase forms, dull-tinted armoured skin, three encounter objects and one illusion.`);
