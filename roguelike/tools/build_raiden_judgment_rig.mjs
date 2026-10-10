// Original dimensional arm and horizontal katana cut for the final calamity.
// Native display geometry; no sampled audio, particles, or borrowed animation.
// Call start at arena origin (0,201,0), tick as the boss reading rdTime, cleanup on cancel.
// node tools/build_raiden_judgment_rig.mjs --resourcepack <resourcepack>
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
Object.assign(textures,{bone:'rlk:player_motion/white_concrete',silver:'rlk:player_motion/light_gray_concrete',blue:'rlk:player_motion/blue_concrete',purple:'rlk:player_motion/purple_concrete',gold:'rlk:cm/fm/metal'});
const sides=['north','south','east','west','up','down'];
const box=(a,b,c,over={})=>({from:a,to:b,shade:false,faces:Object.fromEntries(sides.map(n=>[n,{texture:'#'+(over[n]||c),uv:[0,0,16,16]}]))});
const centered=(p,s,c)=>box(p.map((x,i)=>8+x-s[i]/2),p.map((x,i)=>8+x+s[i]/2),c);
const model=(name,e)=>{json(path.join(assets,'models/item/raiden/judgment',name+'.json'),{ambientocclusion:false,textures:{...textures,particle:textures.violet},elements:e});json(path.join(assets,'items/raiden/judgment',name+'.json'),{model:{type:'minecraft:model',model:'rlk:item/raiden/judgment/'+name}});};
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
// All bones have their proximal pivot at [8,8,8], and extend along local -Y.
function bone(kind){const fore=kind==='forearm',len=fore?16:14,e=[];e.push(box([4.7,8-len,4.7],[11.3,8,11.3],'purple',{north:'blue'}));for(let j=0;j<6;j++){const t=j/5,y=8-len+(j+.5)*len/6,w=(fore?5.5:5.2)+Math.sin(t*Math.PI)*(fore?2.4:1.6);e.push(box([8-w/2,y-len/12-.03,8-w/2],[8+w/2,y+len/12+.03,8+w/2],'bone',{east:'silver',north:'silver'}));}for(const y of[7,8-len+1.0]){e.push(box([4.4,y-.5,4.4],[11.6,y+.5,11.6],'gold'));e.push(box([4.2,y-.13,4.2],[11.8,y+.13,11.8],'white'));}e.push(box([6.4,9-len,4.35],[9.6,5.9,4.68],'purple'));e.push(box([7.72,9.2-len,4.18],[8.28,5.6,4.53],'cyan'));e.push(box([6.4,-.2,4.08],[9.6,.9,4.48],'gold'));e.push(box([7.42,-.7,3.98],[8.58,1.4,4.36],'violet_dense'));return e;}
model('upper_arm',bone('upper'));
model('forearm',bone('forearm'));
// Palm + four curled fingers + opposed thumb, leaving a real passage for the hilt.
const palm=[box([3.7,-1.0,5.9],[12.3,8.0,9.5],'bone',{north:'silver'}),box([3.5,6.7,5.5],[12.5,8.1,9.9],'gold'),box([4.4,1.0,9.55],[11.6,6.2,9.78],'purple'),box([5.4,2.2,9.8],[10.6,4.3,9.99],'gold'),box([7.5,1.5,10.01],[8.5,5,10.22],'white')];
for(let i=0;i<4;i++){const x=4+i*2.03;const bend=.15*Math.abs(i-1.5);palm.push(box([x,-3.4+bend,6.0],[x+1.6,.5,9.2],'bone',{north:'silver'}));palm.push(box([x,-3.4+bend,8.8],[x+1.6,-1.6+bend,13.0],'bone',{down:'silver'}));palm.push(box([x,-1.9+bend,11.55],[x+1.6,1.5+bend,13.15],'bone',{east:'silver'}));palm.push(box([x,-.05+bend,11.5],[x+1.6,.6+bend,13.24],'gold'));palm.push(box([x+.15,1.0+bend,11.6],[x+1.45,1.7+bend,13.24],'purple'));}
palm.push(box([1.7,1.0,6.2],[4.2,5.8,9.7],'bone'));palm.push(box([1.9,-.5,8.7],[4.1,2.6,12.3],'bone',{east:'silver'}));palm.push(box([2.0,-.6,11.4],[6.0,1.4,13.2],'bone'));palm.push(box([5.2,-.5,11.35],[6.8,1.3,13.15],'purple'));
model('closed_hand',palm);
const upperVeins=[],foreVeins=[];for(const s of[-1,1]){upperVeins.push(...line([[s*2.8,-12,-3.85],[s*3.7,-7,-3.95],[s*2.8,-4,-3.9],[s*3.5,-.5,-3.85]],.11,'lavender'));foreVeins.push(...line([[s*2.7,-14,-3.85],[s*3.5,-10,-3.95],[s*2.9,-6,-3.9],[s*3.45,-1,-3.85]],.15,'cyan'));}model('upper_veins',upperVeins);model('forearm_veins',foreVeins);
// Long, subtly curved katana: violet steel, silver bevel, dark spine, bright edge.
const katana=[box([7.6,2,7.6],[8.4,10.1,8.4],'purple',{east:'blue'}),box([7.2,1.5,7.2],[8.8,2.4,8.8],'gold')];for(let y=3;y<9;y+=1.32)katana.push(box([7.56,y,7.56],[8.44,y+.49,8.44],'bone'));
katana.push(box([4,9.1,6.4],[12,10.25,9.6],'gold'),box([5.4,8.7,5.9],[10.6,10.45,10.1],'purple'),box([6.8,10.25,6.7],[9.2,11.1,9.3],'bone'));
for(let i=0;i<26;i++){const y=10.65+i*.76,x=7.8+i*i*.0017,w=1.5*(1-i/30);katana.push(box([x-w/2,y,7.65],[x+w/2,y+.83,8.35],i%4===0?'blue':'purple',{north:'violet_dense',south:'bone',west:'silver'}));katana.push(box([x-w/2-.08,y,7.56],[x-w/2+.18,y+.84,8.44],'white'));katana.push(box([x+w/2-.2,y,7.6],[x+w/2+.06,y+.84,8.4],'blue'));}model('katana',katana);
function bladeGlow(color,extra){const e=[];for(let i=0;i<26;i++){const y=2.65+i*.76,x=-.2+i*i*.0017,w=1.5*(1-i/30)+extra;e.push(centered([x,y+.42,0],[w,.87,.16+extra*.15],color));}return e;}
model('blade_aura',bladeGlow('violet',1.4));
model('blade_haze',bladeGlow('glow',3.9));
model('blade_trail_near',bladeGlow('violet',1));
model('blade_trail_far',bladeGlow('afterglow',.7));
model('blade_trail_faint',bladeGlow('lavender',.3));
for(let v=0;v<2;v++){const e=[];for(const s of[-1,1]){const pts=[];for(let i=0;i<10;i++){const y=3+i*2,x=-.2+i*i*.012+s*(.8+((i+v)%3===0?.9:.15));pts.push([x,y,s*.55]);}e.push(...line(pts,.21,'violet_dense'));e.push(...line(pts.map(p=>[p[0],p[1],p[2]+s*.17]),.07,'white'));for(const n of[2,6]){const p=pts[n];e.push(...line([p,[p[0]+s*1.4,p[1]+1.1,p[2]],[p[0]+s*.9,p[1]+2.3,p[2]],[p[0]+s*2.1,p[1]+3.3,p[2]]],.12,'cyan'));}}model('blade_lightning_'+v,e);}
const fragments=[];for(let i=0;i<14;i++){const a=i*Math.PI*2/14,r=12+rand()*5;fragments.push(centered([Math.cos(a)*r,Math.sin(a)*5,.5+rand()],[.5+rand()*.8,1.0+rand()*1.2,.13],i%3===0?'white':'violet_dense'));}model('rift_fragments',fragments);
// Quaternion helpers. Model coordinates are world-aligned; the final right-Y-pi
// correction cancels Minecraft's additional item-display model rotation.
const rad=x=>x*Math.PI/180;
const mul=(a,b)=>{const[x,y,z,w]=a,[X,Y,Z,W]=b;return[w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W,w*W-x*X-y*Y-z*Z];};
const q=e=>{const[x,y,z]=e.map(v=>rad(v)/2);return mul(mul([0,0,Math.sin(z),Math.cos(z)],[0,Math.sin(y),0,Math.cos(y)]),[Math.sin(x),0,0,Math.cos(x)]);};
const rot=(a,v)=>mul(mul(a,[...v,0]),[-a[0],-a[1],-a[2],a[3]]).slice(0,3);
const add=(a,b)=>a.map((v,i)=>v+b[i]),sub=(a,b)=>a.map((v,i)=>v-b[i]),times=(a,s)=>a.map(v=>v*s),lerp=(a,b,t)=>a.map((v,i)=>v+(b[i]-v)*t),dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0),norm=a=>times(a,1/Math.max(.00001,Math.hypot(...a))),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const clamp=x=>Math.max(0,Math.min(1,x)),smooth=x=>{x=clamp(x);return x*x*(3-2*x);};
function down(v){const n=norm(v),a=[-n[2],0,n[0],1-n[1]];return n[1]>.9999?[1,0,0,0]:norm(a);}
function basisQuat(x,y,z){const m=[x[0],y[0],z[0],x[1],y[1],z[1],x[2],y[2],z[2]],tr=m[0]+m[4]+m[8];let a;if(tr>0){const s=Math.sqrt(tr+1)*2;a=[(m[7]-m[5])/s,(m[2]-m[6])/s,(m[3]-m[1])/s,s/4];}else if(m[0]>m[4]&&m[0]>m[8]){const s=Math.sqrt(1+m[0]-m[4]-m[8])*2;a=[s/4,(m[1]+m[3])/s,(m[2]+m[6])/s,(m[7]-m[5])/s];}else if(m[4]>m[8]){const s=Math.sqrt(1+m[4]-m[0]-m[8])*2;a=[(m[1]+m[3])/s,s/4,(m[5]+m[7])/s,(m[2]-m[6])/s];}else{const s=Math.sqrt(1+m[8]-m[0]-m[4])*2;a=[(m[2]+m[6])/s,(m[5]+m[7])/s,s/4,(m[3]-m[1])/s];}return norm(a);}
function bladeQuat(direction){const y=norm(direction),up=[0,1,0],z=norm(sub(up,times(y,dot(y,up)))),x=norm(cross(y,z));return basisQuat(x,y,z);}
const keys=[
 {t:60,h:[7.3,5.7,-2.6],d:[-.66,.67,.26],el:[5.5,8,-4.7]},
 {t:88,h:[8.5,5.7,-1.4],d:[-.62,.70,.28],el:[6.1,8,-4.0]},
 {t:106,h:[9.2,6.5,-1.4],d:[-.52,.80,.30],el:[6.5,8.6,-3.5]},
 {t:116,h:[9.6,6.9,-1.0],d:[-.35,.87,.34],el:[6.7,8.7,-3.4]},
 {t:120,h:[9.0,4.0,0.0],d:[-.942,-.126,.314],el:[6.3,7.1,-2.8]},
 {t:124,h:[6.6,3.3,.5],d:[-.92,-.02,-.392],el:[5.4,6.5,-2.2]},
 {t:131,h:[5.4,4.0,-1.1],d:[-.91,.25,-.33],el:[4.5,6.9,-3.2]},
 {t:138,h:[5.4,5.1,-2.8],d:[-.76,.61,-.22],el:[4.3,7.8,-4.1]},
 {t:152,h:[2.0,8.5,-6.0],d:[-.52,.81,.27],el:[1.2,9,-6.3]}
];
function motion(t){let a=keys[0],b=a;for(const k of keys){if(k.t<=t)a=k;else{b=k;break;}b=a;}const u=a===b?0:clamp((t-a.t)/(b.t-a.t));const f=b.t===120?u*u:a.t===120?1-(1-u)*(1-u):smooth(u);return Object.fromEntries(['h','d','el'].map(n=>[n,lerp(a[n],b[n],f)]));}
const parts={rift_void:'rift_void',rift_depth:'rift_depth',rift_haze:'rift_haze',rift_edge:'rift_edge_0',rift_edge_glow:'rift_edge_glow',rift_stars:'rift_stars',rift_iris:'rift_iris',rift_fragments:'rift_fragments',upper:'upper_arm',forearm:'forearm',hand:'closed_hand',upper_veins:'upper_veins',forearm_veins:'forearm_veins',sword:'katana',blade_aura:'blade_aura',blade_haze:'blade_haze',blade_lightning:'blade_lightning_0',trail1:'blade_trail_near',trail2:'blade_trail_far',trail3:'blade_trail_faint'};
function sword(t){const m=motion(t),emerge=smooth((t-54)/34),exit=1-smooth((t-138)/14),scale=emerge*exit,shoulder=[0,9.1,-6.6],h=lerp(shoulder,m.h,emerge),Q=bladeQuat(m.d);return{t:h,q:Q,s:[12.2*scale,12.2*scale,12.2*scale]};}
function pose(t){
 const m=motion(t),opening=smooth((t-24)/22),openHeight=.035+.965*smooth((t-38)/27),closing=1-smooth((t-140)/14),pulse=1+.025*Math.sin(t*.34),portal=[0,9.15,-6.8],portalQ=q([70,0,0]),o={};
 const portalScale=[5.5*opening*closing,5.5*openHeight*closing,5.5*closing];
 for(const n of ['rift_void','rift_depth','rift_haze','rift_edge','rift_edge_glow','rift_stars','rift_iris','rift_fragments'])o[n]={t:[...portal],q:[...portalQ],s:[...portalScale]};
 o.rift_depth.t=add(portal,rot(portalQ,[0,0,-.03]));
 o.rift_haze.t=add(portal,rot(portalQ,[0,0,-.06]));o.rift_haze.s=times(portalScale,1.10*pulse);
 o.rift_edge_glow.s=times(portalScale,1.025*pulse);
 o.rift_stars.q=mul(portalQ,q([0,0,Math.sin(t*.018)*5]));o.rift_iris.q=mul(portalQ,q([0,0,t*.5]));
 o.rift_fragments.q=mul(portalQ,q([0,0,Math.sin(t*.11)*3]));o.rift_fragments.s=times(portalScale,1.0+.065*Math.sin(t*.085));
 o.rift_edge.model='rift_edge_'+(Math.floor(t/3)%2);
 const sw=sword(t),size=sw.s[0]/12.2,sh=[0,9.1,-6.6],handQ=mul(sw.q,q([0,0,90])),handSize=4.4*size;
 // The hilt runs through the curled fingers: hand local +X = katana local +Y.
 const wrist=sub(sw.t,rot(handQ,times([0,-.53,.155],handSize)));
 const el=lerp(sh,m.el,smooth((t-54)/34));
 o.upper={t:sh,q:down(sub(el,sh)),s:[3.4*size,Math.hypot(...sub(el,sh))/.875,3.4*size]};
 o.forearm={t:el,q:down(sub(wrist,el)),s:[3.9*size,Math.hypot(...sub(wrist,el)),3.9*size]};
 o.hand={t:wrist,q:handQ,s:[handSize,handSize,handSize]};
 o.upper_veins=structuredClone(o.upper);o.forearm_veins=structuredClone(o.forearm);
 if(size<.0001)for(const n of['upper','forearm','hand','upper_veins','forearm_veins'])o[n].s=[0,0,0];
 o.sword=sw;
 for(const n of['blade_aura','blade_haze','blade_lightning'])o[n]=structuredClone(sw);
 o.blade_lightning.model='blade_lightning_'+(Math.floor(t/2)%2);
 for(let i=1;i<=3;i++){o['trail'+i]=sword(t-i*.65);if(t<117||t>128)o['trail'+i].s=[0,0,0];}
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
console.log(`Built final calamity: ${Object.keys(parts).length} displays, 177 poses; horizontal cut reaches contact at tick120.`);
