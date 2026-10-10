// Original elemental-mage and archer rigs for roguelike. No reference motion/assets copied.
// node tools/build_casters_archer.mjs --datapack <folder> --resourcepack <unpacked folder>
// Shared lifecycle hooks and atlas registration are intentionally managed by the pack integrator.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const base=path.dirname(fileURLToPath(import.meta.url));
const arg=n=>{const i=process.argv.indexOf(n);return i<0?undefined:process.argv[i+1];};
const dpRoot=path.resolve(arg('--datapack')||path.join(base,'..'));
if(!arg('--resourcepack'))throw Error('Provide --resourcepack with the unpacked resource pack.');
const rpRoot=path.resolve(arg('--resourcepack'));
if(!fs.existsSync(path.join(dpRoot,'pack.mcmeta'))||!fs.existsSync(path.join(rpRoot,'pack.mcmeta')))throw Error('Each target must contain pack.mcmeta.');
const dp=path.join(dpRoot,'data/rlk/function/cm'),rp=path.join(rpRoot,'assets/rlk');
const put=(p,s)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,s.endsWith('\n')?s:s+'\n','utf8');};
const fn=(p,s)=>put(path.join(dp,p+'.mcfunction'),s);
const json=(p,s)=>put(p,JSON.stringify(s,null,2));
function faces(u,v,w,h,d){const face=(x1,y1,x2,y2)=>({uv:[x1/4,y1/4,x2/4,y2/4],texture:'#skin',tintindex:0});return {east:face(u,v+d,u+d,v+d+h),north:face(u+d,v+d,u+d+w,v+d+h),west:face(u+d+w,v+d,u+2*d+w,v+d+h),south:face(u+2*d+w,v+d,u+2*d+2*w,v+d+h),up:face(u+d,v,u+d+w,v+d),down:face(u+d+w,v+d,u+d+2*w,v)};}
const box=(from,to,uv,i=0)=>({from:from.map(v=>v-i),to:to.map(v=>v+i),faces:faces(...uv)});
const solid=(from,to,texture,uv=[0,0,16,16])=>({from,to,faces:Object.fromEntries(['north','south','east','west','up','down'].map(f=>[f,{texture:'#'+texture,uv,tintindex:0}]))});
const humanoid={
 head:{from:[4,8,4],to:[12,16,12],uv:[0,0,8,8,8],over:[32,0,8,8,8],inflate:.5},
 body:{from:[4,-4,6],to:[12,8,10],uv:[16,16,8,12,4],over:[16,32,8,12,4],inflate:.25},
 right_arm:{from:[6,-2,6],to:[10,10,10],uv:[40,16,4,12,4],over:[40,32,4,12,4],inflate:.25},
 left_arm:{from:[6,-2,6],to:[10,10,10],uv:[32,48,4,12,4],over:[48,48,4,12,4],inflate:.25},
 right_leg:{from:[6,-4,6],to:[10,8,10],uv:[0,16,4,12,4],over:[0,32,4,12,4],inflate:.25},
 left_leg:{from:[6,-4,6],to:[10,8,10],uv:[16,48,4,12,4],over:[0,48,4,12,4],inflate:.25}
};
const kinds=['fm','im','ar'];
const aliases={fm:{wood:'dark_oak_planks',metal:'gold_block',gem:'magma'},im:{wood:'stripped_birch_log',metal:'iron_block',gem:'blue_ice'},ar:{wood:'dark_oak_planks',metal:'iron_block',string:'white_wool'}};
const atlasSources=[];
for(const kind of kinds){
 for(const [name,s] of Object.entries(humanoid))json(path.join(rp,'models/item/cm',kind,name+'.json'),{ambientocclusion:false,textures:{skin:'rlk:skin/mob_'+kind,particle:'rlk:skin/mob_'+kind},elements:[box(s.from,s.to,s.uv),box(s.from,s.to,s.over,s.inflate)]});
 atlasSources.push({type:'minecraft:single',resource:'rlk:skin/mob_'+kind});
 for(const [name,resource] of Object.entries(aliases[kind]))atlasSources.push({type:'minecraft:single',resource:'minecraft:block/'+resource,sprite:'rlk:cm/'+kind+'/'+name});
 const textures=Object.fromEntries(Object.keys(aliases[kind]).map(n=>[n,'rlk:cm/'+kind+'/'+n]));textures.particle=textures.wood;
 if(kind!=='ar'){
  const e=[solid([7.3,0,7.3],[8.7,19,8.7],'wood'),solid([6.9,0,6.9],[9.1,2,9.1],'metal'),solid([6.8,17,6.8],[9.2,19,9.2],'metal'),solid([5.5,19,6.5],[6.8,23,9.5],'metal'),solid([9.2,19,6.5],[10.5,23,9.5],'metal')];
  if(kind==='fm')e.push(solid([6,20,6],[10,24,10],'gem'),solid([7,24,7],[9,25.5,9],'gem'),solid([6.2,18.5,6.2],[9.8,20,9.8],'metal'));
  else e.push(solid([6,20,6],[10,23.5,10],'gem'),solid([7,23.5,7],[9,25.5,9],'gem'),solid([7,18.5,7],[9,20,9],'gem'));
  json(path.join(rp,'models/item/cm',kind,'staff.json'),{ambientocclusion:false,textures,elements:e});
 }else{
  // Bow rests in a Y/Z plane: recurved limbs face forward (-Z), tips carry real geometric strings.
  json(path.join(rp,'models/item/cm/ar/bow.json'),{ambientocclusion:false,textures,elements:[solid([7.35,5.7,7.35],[8.65,10.3,8.65],'wood'),solid([7.45,10.3,6.7],[8.55,13.6,8],'wood'),solid([7.45,13.6,7.1],[8.55,16.4,8.4],'wood'),solid([7.45,16.4,8],[8.55,18,9.3],'wood'),solid([7.45,2.4,6.7],[8.55,5.7,8],'wood'),solid([7.45,-.4,7.1],[8.55,2.4,8.4],'wood'),solid([7.45,-2,8],[8.55,-.4,9.3],'wood'),solid([7.1,6.7,7.1],[8.9,9.3,8.9],'metal')]});
  // Unit vertical rods are fitted to endpoints per pose. Their origin is the grip-centred [8,8,8].
  for(const p of ['string_upper','string_lower'])json(path.join(rp,'models/item/cm/ar',p+'.json'),{ambientocclusion:false,textures,elements:[solid([7.88,0,7.88],[8.12,16,8.12],'string')]});
  json(path.join(rp,'models/item/cm/ar/arrow.json'),{ambientocclusion:false,textures,elements:[solid([7.78,7.78,-7],[8.22,8.22,10],'wood'),solid([7.2,7.6,-8.5],[8.8,8.4,-6.5],'metal'),solid([7.1,7.85,8],[8.9,8.15,10.7],'string')]});
 }
}
const rad=x=>x*Math.PI/180;
function mul(a,b){const[x,y,z,w]=a,[X,Y,Z,W]=b;return[w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W,w*W-x*X-y*Y-z*Z];}
function q(e=[0,0,0]){const[x,y,z]=e.map(v=>rad(v)/2);return mul(mul([0,0,Math.sin(z),Math.cos(z)],[0,Math.sin(y),0,Math.cos(y)]),[Math.sin(x),0,0,Math.cos(x)]);}
function rot(q,v){return mul(mul(q,[...v,0]),[-q[0],-q[1],-q[2],q[3]]).slice(0,3);}
const add=(a,b)=>a.map((v,i)=>v+b[i]),sub=(a,b)=>a.map((v,i)=>v-b[i]);
function rod(a,b){const d=sub(b,a),l=Math.hypot(...d),v=d.map(x=>x/l);let quat=v[1]<-.999999?[1,0,0,0]:[v[2],0,-v[0],1+v[1]];const n=Math.hypot(...quat);quat=quat.map(x=>x/n);return {t:a.map((x,i)=>(x+b[i])/2),q:quat,s:[1,l,1]};}
const mageBase={torso:[3,0,0],head:[-3,0,0],right_arm:[22,-8,-10],left_arm:[10,0,10],right_leg:[-3,0,-3],left_leg:[3,0,3],weapon:[-22,0,10]};
const archerBase={torso:[3,-9,0],head:[-3,9,0],right_arm:[18,0,-8],left_arm:[30,8,10],right_leg:[-4,0,-3],left_leg:[4,0,3],weapon:[-30,0,-10],draw:false};
function rig(kind,over={}){
 const p={...(kind==='ar'?archerBase:mageBase),...over};
 const hip=add([0,.75,0],p.shift||[0,0,0]),torso=q(p.torso),root=q(p.root||[0,0,0]),r={};
 const shoulder=add(hip,rot(torso,[0,.75,0]));
 r.body={t:shoulder,q:torso};r.head={t:shoulder,q:mul(torso,q(p.head))};
 for(const [part,sign] of [['right_arm',-1],['left_arm',1]])r[part]={t:add(hip,rot(torso,[sign*.375,.625,0])),q:mul(torso,q(p[part]))};
 for(const [part,sign] of [['right_leg',-1],['left_leg',1]])r[part]={t:add(hip,[sign*.125,0,0]),q:q(p[part])};
 if(kind!=='ar'){
  const hand=r.right_arm;r.staff={t:add(hand.t,rot(hand.q,[0,-.535,-.015])),q:mul(hand.q,q(p.weapon))};
 }else{
  // Counter-rotate at the wrist: the bow stays upright and its arrow tracks -Z,
  // while torso/shoulders perform the draw. The grip remains exactly in the hand.
  const hand=r.left_arm;r.bow={t:add(hand.t,rot(hand.q,[0,-.535,-.015])),q:q(p.bowRotation||[0,0,0])};
  const upper=add(r.bow.t,rot(r.bow.q,[0,.59,.055])),lower=add(r.bow.t,rot(r.bow.q,[0,-.59,.055]));
  const pull=p.draw?add(r.right_arm.t,rot(r.right_arm.q,[0,-.535,-.015])):add(r.bow.t,rot(r.bow.q,[0,0,.055]));
  r.string_upper=rod(upper,pull);r.string_lower=rod(lower,pull);
  r.arrow={t:pull,q:r.bow.q,s:p.draw?[1,1,1]:[.001,.001,.001]};
 }
 for(const a of Object.values(r)){
  a.t=add(p.rootShift||[0,0,0],rot(root,a.t).map(v=>v*(p.size??1)));a.q=mul(root,a.q);a.s=(a.s||[1,1,1]).map(v=>v*(p.size??1));
  // Authored -Z forward -> runtime +Z forward; renderer Y180 is applied after the NBT transform.
  a.t=[a.t[0],a.t[1],-a.t[2]];a.q=[-a.q[0],-a.q[1],a.q[2],a.q[3]];
 }
 return r;
}
const fl=n=>(Math.abs(n)<.0000005?'0':String(Number(n.toFixed(6))))+'f',arr=a=>'['+a.map(fl).join(',')+']';
const authored={};
for(const kind of kinds){
 const isAr=kind==='ar',parts=[...Object.keys(humanoid),...(isAr?['bow','string_upper','string_lower','arrow']:['staff'])],poses=[];
 for(const p of parts)json(path.join(rp,'items/cm',kind,p+'.json'),{model:{type:'minecraft:model',model:'rlk:item/cm/'+kind+'/'+p,tints:[{type:'minecraft:custom_model_data',index:0,default:16777215}]}});
 const pose=(id,name,duration,over)=>{const r=rig(kind,over);poses.push({id,name,duration,rig:r});fn(kind+'/rig/pose/'+id,`# Original ${kind} pose: ${name}.\n`+parts.map(p=>`data merge entity @e[tag=rlk_${kind}_this,tag=rlk_${kind}_${p},limit=1] {start_interpolation:0,interpolation_duration:${duration},transformation:{translation:${arr(r[p].t)},left_rotation:${arr(r[p].q)},scale:${arr(r[p].s)},right_rotation:[0f,0f,0f,1f]}}`).join('\n'));};
 for(let i=0;i<4;i++){const a=i*Math.PI/2,s=Math.sin(a);pose(i,'breathing_'+i,12,{shift:[0,s*.013,0],torso:[3+s,0,Math.cos(a)*.5],head:[-3-s,0,0]});}
 for(let i=0;i<8;i++){const a=i*Math.PI/4,s=Math.sin(a);pose(10+i,'advance_'+i,3,{shift:[0,Math.abs(Math.cos(a))*.025,0],torso:[6,s*3,-s],head:[-6,-s*3,0],right_arm:isAr?[18-s*17,0,-8]:[22-s*5,-8,-10],left_arm:isAr?[30+s*4,8,10]:[10+s*20,0,10],right_leg:[s*27,0,-3],left_leg:[-s*27,0,3]});}
 if(!isAr){
  const side=kind==='fm'?1:-1;
  pose(20,'gather_magic',3,{shift:[0,-.035,0],torso:[-3,side*5,-2],head:[-10,-side*5,0],right_arm:[61,4,-27],left_arm:[64,-4,28],weapon:[-38,0,10]});
  pose(21,'arms_high',3,{torso:[-7,side*9,-3],head:[-13,-side*9,0],right_arm:[133,7,-34],left_arm:[137,-7,33],weapon:[-63,5,16]});
  pose(22,'overhead_begin',3,{shift:[0,.025,0],torso:[-6,side*11,-3],head:[-8,-side*11,0],right_arm:[166,10,-33],left_arm:[159,-10,30],weapon:[-77,8,14]});
  for(let i=0;i<8;i++){const a=i*Math.PI/4,s=Math.sin(a),c=Math.cos(a);pose(23+i,'overhead_staff_circle_'+i,2,{shift:[0,.018+c*.013,0],torso:[-6+c*2,side*8+s*9,-s*3],head:[-9,-side*8-s*9,s*2],right_arm:[161+c*11,10+s*25,-32+s*10],left_arm:[158-c*8,-9-s*18,31-c*7],weapon:[-75-s*17,side*c*24,12+s*26]});}
  pose(31,'gather_for_cast',2,{shift:[0,-.025,.018],torso:[-8,18,-4],head:[2,-18,0],right_arm:[145,-12,-26],left_arm:[131,15,24],weapon:[110,-8,12]});
  pose(32,'cast_ready',1,{shift:[0,-.03,-.01],torso:[3,9,-2],head:[-3,-9,0],right_arm:[117,-11,-14],left_arm:[112,9,15],weapon:[146,0,2]});
  pose(40,'cast_forward',1,{shift:[0,-.04,-.09],torso:[11,-8,2],head:[-11,8,0],right_arm:[98,-12,-10],left_arm:[103,12,13],weapon:[168,0,0]});
  pose(41,'cast_follow_through',2,{shift:[0,-.045,-.1],torso:[13,-11,3],head:[-13,11,0],right_arm:[94,-11,-12],left_arm:[96,13,15],weapon:[174,0,0]});
  pose(42,'recall_staff',3,{shift:[0,-.015,-.025],torso:[4,1,0],head:[-4,-1,0],right_arm:[63,-10,-18],left_arm:[60,12,21],weapon:[-54,0,9]});
  pose(43,'settle_magic',3,{right_arm:[32,-9,-12],left_arm:[28,4,15],weapon:[-32,0,10]});
 }else{
  pose(20,'raise_bow',4,{torso:[4,-17,0],head:[-4,17,0],left_arm:[63,18,8],right_arm:[48,-28,-9],weapon:[-63,-18,-8],draw:false});
  pose(21,'nock_arrow',4,{torso:[0,-28,0],head:[0,28,0],left_arm:[90,45,0],right_arm:[90,-45,0],draw:true});
  pose(22,'draw_half',4,{shift:[0,-.012,.014],torso:[0,-28,-1],head:[0,28,1],left_arm:[90,45,0],right_arm:[90,-62,0],draw:true});
  pose(23,'draw_full',3,{shift:[0,-.016,.025],torso:[0,-28,-2],head:[0,28,2],left_arm:[90,45,0],right_arm:[90,-80,0],draw:true});
  pose(24,'aim_locked',2,{shift:[0,-.015,.018],torso:[0,-28,-2],head:[0,28,2],left_arm:[90,45,0],right_arm:[90,-80,0],draw:true});
  pose(40,'release_string',1,{shift:[0,-.012,.032],torso:[-2,-30,-3],head:[2,30,3],left_arm:[90,47,0],right_arm:[95,-97,0],draw:false});
  pose(41,'bow_recoil',2,{shift:[0,-.014,.02],torso:[-1,-29,-2],head:[1,29,2],left_arm:[92,46,2],right_arm:[85,-99,-5],draw:false});
  pose(42,'lower_bow',3,{torso:[3,-19,-1],head:[-3,19,1],left_arm:[67,16,12],right_arm:[24,-23,-25],weapon:[-67,-16,-12],draw:false});
  pose(43,'settle_bow',3,archerBase);
 }
 pose(50,'hit_recoil',2,{shift:[0,-.06,.04],torso:[-12,8,-8],head:[13,-8,5],right_arm:[38,5,-23],left_arm:[41,-9,26],right_leg:[-10,0,-6],left_leg:[15,0,6]});
 pose(51,'hit_recover',3,{shift:[0,-.028,.016],torso:[-3,3,-3],head:[4,-3,2],right_arm:[28,2,-16],left_arm:[29,-4,19]});
 pose(60,'death_buckle',2,{shift:[0,-.18,0],torso:[24,-8,14],head:[17,8,8],right_arm:[37,6,-27],left_arm:[29,-8,32],right_leg:[-24,0,-13],left_leg:[31,0,13]});
 pose(61,'death_fall',4,{root:[5,0,55],rootShift:[0,.20,0],torso:[9,-4,8],head:[14,5,7],right_arm:[24,2,-15],left_arm:[15,9,17],right_leg:[-10,0,-4],left_leg:[18,0,5]});
 pose(62,'death_land',3,{root:[0,0,89],rootShift:[0,.30,0],torso:[6,0,0],head:[12,-8,4],right_arm:[22,0,-18],left_arm:[8,6,10],right_leg:[-8,0,0],left_leg:[15,0,3]});
 pose(63,'death_dissolve',4,{root:[0,0,89],rootShift:[0,.10,0],torso:[6,0,0],head:[12,-8,4],right_arm:[22,0,-18],left_arm:[8,6,10],right_leg:[-8,0,0],left_leg:[15,0,3],size:.04});
 authored[kind]={parts,poses};
 fn(kind+'/rig/apply',poses.filter(p=>p.id<60).map(p=>`execute if score #${kind}Pose tmp matches ${p.id} run function rlk:cm/${kind}/rig/pose/${p.id}`).join('\n'));
 fn(kind+'/rig/select',`# Exact numeric owner, including corpses; never nearest-entity ownership.\ntag @e[tag=rlk_${kind}_this] remove rlk_${kind}_this\nscoreboard players operation #${kind}Id tmp = @s cmId\nexecute as @e[tag=rlk_${kind}_rig] if score @s cmId = #${kind}Id tmp run tag @s add rlk_${kind}_this`);
 fn(kind+'/rig/rebuild',`function rlk:cm/${kind}/rig/select\nkill @e[tag=rlk_${kind}_this]\nexecute as @e[tag=rlk_cmv] if score @s cmId = #${kind}Id tmp run kill @s\nscoreboard players set @s cmAF 0\nscoreboard players set @s cmAH 0\nscoreboard players set @s cmAR 0\nscoreboard players set @s cmAP -1\nexecute store result score @s cmAX run data get entity @s Pos[0] 1000\nexecute store result score @s cmAZ run data get entity @s Pos[2] 1000\nfunction rlk:cm/${kind}/rig/create`);
 let create=`summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_${kind}_rig","rlk_${kind}_anchor","rlk_cmlink","rlk_cmsync","rlk_${kind}_new"]}\n`;
 for(const p of parts)create+=`summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_pet","rlk_${kind}_rig","rlk_${kind}_part","rlk_${kind}_${p}","rlk_cmlink","rlk_cmsync","rlk_${kind}_new"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:1.5f,width:4f,height:4f,shadow_radius:0f,${p==='staff'?'brightness:{sky:15,block:15},':''}item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:cm/${kind}/${p}","minecraft:custom_model_data":{colors:[16777215]}}}}\n`;
 create+=`scoreboard players operation @e[tag=rlk_${kind}_new] cmId = #${kind}Id tmp\ntag @e[tag=rlk_${kind}_new] add rlk_${kind}_this\ntag @e[tag=rlk_${kind}_new] remove rlk_${kind}_new\nscoreboard players set @e[tag=rlk_${kind}_this,tag=rlk_${kind}_anchor] cmAD 0\nfunction rlk:cm/${kind}/rig/pose/0\ntag @e[tag=rlk_${kind}_this] remove rlk_${kind}_this`;
 fn(kind+'/rig/create',create);
 fn(kind+'/rig/hurt',`scoreboard players set @s cmAH 6\nfunction rlk:cm/${kind}/rig/select\nexecute as @e[tag=rlk_${kind}_this,tag=rlk_${kind}_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16737903]}\ntag @e[tag=rlk_${kind}_this] remove rlk_${kind}_this`);
 fn(kind+'/rig/tick',`# @s = living brain. Existing gameplay timers are read, not changed, by this rig.\nfunction rlk:cm/${kind}/rig/select\nexecute store result score #${kind}Count tmp if entity @e[tag=rlk_${kind}_this]\nexecute unless score #${kind}Count tmp matches ${parts.length+1} run function rlk:cm/${kind}/rig/rebuild\nexecute unless score #${kind}Count tmp matches ${parts.length+1} run function rlk:cm/${kind}/rig/select\n# Preserve ALL owner-linked projectiles and telegraph attachments, in addition to the rig.\nexecute as @e[tag=rlk_cmlink] if score @s cmId = #${kind}Id tmp run tag @s add rlk_cmsync\nexecute ${isAr?'unless score @s cmAR matches 1.. ':''}facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 as @e[tag=rlk_${kind}_this] run tp @s ~ ~ ~ ~ 0\n${isAr?'# Keep the released arrow heading through recoil, while still following the brain position.\nexecute if score @s cmAR matches 1.. as @e[tag=rlk_ar_this] rotated as @s run tp @s ~ ~ ~ ~ 0\n':''}${isAr?`# The final draw follows the already-locked projectile heading.\nexecute if score @s cmS matches 1 if score @s cmT <= #cmW_arL tmp as @e[tag=rlk_cmline,distance=..8] if score @s cmId = #arId tmp rotated as @s rotated ~ 0 as @e[tag=rlk_ar_this] run tp @s ~ ~ ~ ~ 0\n`:''}execute store result score #${kind}X tmp run data get entity @s Pos[0] 1000\nexecute store result score #${kind}Z tmp run data get entity @s Pos[2] 1000\nscoreboard players operation #${kind}DX tmp = #${kind}X tmp\nscoreboard players operation #${kind}DZ tmp = #${kind}Z tmp\nscoreboard players operation #${kind}DX tmp -= @s cmAX\nscoreboard players operation #${kind}DZ tmp -= @s cmAZ\nscoreboard players set #${kind}Neg tmp -1\nexecute if score #${kind}DX tmp matches ..-1 run scoreboard players operation #${kind}DX tmp *= #${kind}Neg tmp\nexecute if score #${kind}DZ tmp matches ..-1 run scoreboard players operation #${kind}DZ tmp *= #${kind}Neg tmp\nscoreboard players operation #${kind}Move tmp = #${kind}DX tmp\nscoreboard players operation #${kind}Move tmp += #${kind}DZ tmp\nscoreboard players operation @s cmAX = #${kind}X tmp\nscoreboard players operation @s cmAZ = #${kind}Z tmp\nexecute if score @s cmAH matches 1 as @e[tag=rlk_${kind}_this,tag=rlk_${kind}_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}\nexecute if score @s frzT matches 1.. run return run function rlk:cm/${kind}/rig/frozen\nscoreboard players add @s cmAF 1\nexecute if score @s cmAF matches 48.. run scoreboard players set @s cmAF 0\nscoreboard players operation #${kind}Frame tmp = @s cmAF\nscoreboard players set #${kind}Div tmp 12\nscoreboard players operation #${kind}Frame tmp /= #${kind}Div tmp\nscoreboard players operation #${kind}Pose tmp = #${kind}Frame tmp\nexecute if score #${kind}Move tmp matches 8.. run function rlk:cm/${kind}/rig/walk\nexecute if score @s cmS matches 1 run function rlk:cm/${kind}/rig/charge\n${kind==='fm'?'execute if score @s cmS matches 2 run function rlk:cm/fm/rig/volley\n':''}# A confirmed launch/cast sets cmAR; visual recoil is synced to that same tick.\nexecute if score @s cmAR matches 10.. run scoreboard players set #${kind}Pose tmp 40\nexecute if score @s cmAR matches 7..9 run scoreboard players set #${kind}Pose tmp 41\nexecute if score @s cmAR matches 4..6 run scoreboard players set #${kind}Pose tmp 42\nexecute if score @s cmAR matches 1..3 run scoreboard players set #${kind}Pose tmp 43\n${kind==='fm'?'execute if score @s cmS matches 2 if score @s cmAR matches 1.. run function rlk:cm/fm/rig/volley_recover\n':''}# Charge immunity also suppresses visual interruption; the red flash still appears.\nexecute unless entity @s[tag=rlk_cmch] unless score @s cmAR matches 1.. if score @s cmAH matches 4.. run scoreboard players set #${kind}Pose tmp 50\nexecute unless entity @s[tag=rlk_cmch] unless score @s cmAR matches 1.. if score @s cmAH matches 1..3 run scoreboard players set #${kind}Pose tmp 51\nexecute unless score @s cmAP = #${kind}Pose tmp run function rlk:cm/${kind}/rig/apply\nscoreboard players operation @s cmAP = #${kind}Pose tmp\nexecute if score @s cmAR matches 1.. run scoreboard players remove @s cmAR 1\nexecute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1\ntag @e[tag=rlk_${kind}_this] remove rlk_${kind}_this`);
 fn(kind+'/rig/walk',`scoreboard players operation #${kind}Frame tmp = @s cmAF\nscoreboard players set #${kind}Div tmp 24\nscoreboard players operation #${kind}Frame tmp %= #${kind}Div tmp\nscoreboard players set #${kind}Div tmp 3\nscoreboard players operation #${kind}Frame tmp /= #${kind}Div tmp\nscoreboard players operation #${kind}Pose tmp = #${kind}Frame tmp\nscoreboard players add #${kind}Pose tmp 10`);
 fn(kind+'/rig/frozen',`execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1\ntag @e[tag=rlk_${kind}_this] remove rlk_${kind}_this`);
 if(!isAr){
  fn(kind+'/rig/charge',`# Raised arms, then an original eight-keyframe overhead staff circle.\nscoreboard players operation #${kind}Elapsed tmp = #cmW_${kind} tmp\nscoreboard players operation #${kind}Elapsed tmp -= @s cmT\nscoreboard players operation #${kind}Phase tmp = #${kind}Elapsed tmp\nscoreboard players set #${kind}Div tmp 100\nscoreboard players operation #${kind}Phase tmp *= #${kind}Div tmp\nscoreboard players operation #${kind}Div tmp = #cmW_${kind} tmp\nexecute if score #${kind}Div tmp matches ..0 run scoreboard players set #${kind}Div tmp 1\nscoreboard players operation #${kind}Phase tmp /= #${kind}Div tmp\nscoreboard players operation #${kind}Frame tmp = #${kind}Elapsed tmp\nscoreboard players set #${kind}Div tmp 16\nscoreboard players operation #${kind}Frame tmp %= #${kind}Div tmp\nscoreboard players set #${kind}Div tmp 2\nscoreboard players operation #${kind}Frame tmp /= #${kind}Div tmp\nscoreboard players operation #${kind}Pose tmp = #${kind}Frame tmp\nscoreboard players add #${kind}Pose tmp 23\nexecute if score #${kind}Phase tmp matches ..12 run scoreboard players set #${kind}Pose tmp 20\nexecute if score #${kind}Phase tmp matches 13..27 run scoreboard players set #${kind}Pose tmp 21\nexecute if score #${kind}Phase tmp matches 28..38 run scoreboard players set #${kind}Pose tmp 22\n${kind==='im'?`execute if score @s cmT matches 3..5 run scoreboard players set #imPose tmp 31\nexecute if score @s cmT matches 1..2 run scoreboard players set #imPose tmp 32`:''}`);
 }else fn('ar/rig/charge',`# Normalize draw progression to the configured attack windup.\nscoreboard players operation #arElapsed tmp = #cmW_ar tmp\nscoreboard players operation #arElapsed tmp -= @s cmT\nscoreboard players set #arDiv tmp 100\nscoreboard players operation #arElapsed tmp *= #arDiv tmp\nscoreboard players operation #arDiv tmp = #cmW_ar tmp\nexecute if score #arDiv tmp matches ..0 run scoreboard players set #arDiv tmp 1\nscoreboard players operation #arElapsed tmp /= #arDiv tmp\nscoreboard players set #arPose tmp 23\nexecute if score #arElapsed tmp matches ..19 run scoreboard players set #arPose tmp 20\nexecute if score #arElapsed tmp matches 20..39 run scoreboard players set #arPose tmp 21\nexecute if score #arElapsed tmp matches 40..64 run scoreboard players set #arPose tmp 22\nexecute if score @s cmT <= #cmW_arL tmp run scoreboard players set #arPose tmp 24`);
 fn(kind+'/rig/die',`function rlk:cm/${kind}/rig/select\ntag @e[tag=rlk_${kind}_this] add rlk_${kind}_dying\nscoreboard players set @s cmAD 0\nexecute as @e[tag=rlk_${kind}_this,tag=rlk_${kind}_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}\nfunction rlk:cm/${kind}/rig/pose/60\ntag @e[tag=rlk_${kind}_this] remove rlk_${kind}_this`);
 fn(kind+'/rig/death_tick',`function rlk:cm/${kind}/rig/select\nscoreboard players add @s cmAD 1\nexecute if score @s cmAD matches 3 run function rlk:cm/${kind}/rig/pose/61\nexecute if score @s cmAD matches 7 run function rlk:cm/${kind}/rig/pose/62\nexecute if score @s cmAD matches 10 run function rlk:cm/${kind}/rig/pose/63\nexecute if score @s cmAD matches 14.. run kill @e[tag=rlk_${kind}_this]\ntag @e[tag=rlk_${kind}_this] remove rlk_${kind}_this`);
 let spawn=fs.readFileSync(path.join(dp,'spawn',kind+'.mcfunction'),'utf8').replace(/\r\n/g,'\n');
 spawn=spawn.split('\n').filter(l=>!l.includes('minecraft:mannequin')&&!l.includes('rlk_cmvnew')).join('\n').replace('# 커스텀 몹 소환(실행 위치): 두뇌(투명 허스크) + 모습(마네킹)',`# ${kind}: 기존 허스크 두뇌 + cmId로 연결한 원본 디스플레이 리그`);
 fn('spawn/'+kind,spawn);
 function insertOnce(file,anchor,line){const p=path.join(dp,file+'.mcfunction');let s=fs.readFileSync(p,'utf8').replace(/\r\n/g,'\n');if(!s.includes(line)){if(!s.includes(anchor))throw Error('Missing anchor: '+file);s=s.replace(anchor,anchor+'\n'+line);put(p,s);}}
 insertOnce(kind+'/start','scoreboard players set @s cmS 1','scoreboard players set @s cmAR 0');
 if(kind==='fm')insertOnce('fm/shot','scoreboard players operation #fn tmp = @s cmN','scoreboard players set @s cmAR 11');
 if(kind==='im')insertOnce('im/cast','scoreboard players set @s cmS 0','scoreboard players set @s cmAR 11');
 if(kind==='ar')insertOnce('ar/fire','scoreboard players set @s cmS 0','scoreboard players set @s cmAR 11');
}
fn('fm/rig/volley',`# Keep the staff overhead between fireballs, then gather and thrust for each actual launch.\nscoreboard players set #fmPose tmp 31\nexecute if score @s cmT matches 1..2 run scoreboard players set #fmPose tmp 32`);
fn('fm/rig/volley_recover',`# During the three-shot volley, pull back and ready the next thrust in time for its launch.\nexecute if score @s cmAR matches 4..7 run scoreboard players set #fmPose tmp 31\nexecute if score @s cmAR matches 1..3 run scoreboard players set #fmPose tmp 32`);
json(path.join(base,'casters_archer_poses.json'),{authoring:'Original author-authored keyframes for roguelike; 20 ticks/second. No reference geometry or animation copied.',space:'Runtime +Z forward, right hand -X; reflected from authored -Z forward before renderer Y180.',atlasSources,kinds:authored});
console.log(JSON.stringify({generated:kinds,poses:Object.fromEntries(kinds.map(k=>[k,authored[k].poses.length])),atlasSources},null,2));
