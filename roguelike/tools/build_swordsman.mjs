// Original roguelike swordsman rig. No reference-pack geometry or keyframes are copied.
// Run: node tools/build_swordsman.mjs --datapack <pack folder> --resourcepack <unpacked resource pack folder>
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const base=path.dirname(fileURLToPath(import.meta.url));
const arg=(name)=>{const i=process.argv.indexOf(name);return i<0?undefined:process.argv[i+1];};
const dpRoot=path.resolve(arg('--datapack') || path.join(base,'..'));
const rpArg=arg('--resourcepack');
if(!rpArg)throw new Error('Provide --resourcepack pointing to an unpacked rlk resource pack.');
const rpRoot=path.resolve(rpArg);
if(!fs.existsSync(path.join(dpRoot,'pack.mcmeta'))||!fs.existsSync(path.join(rpRoot,'pack.mcmeta')))throw new Error('Both targets must contain pack.mcmeta.');
const dp=path.join(dpRoot,'data/rlk/function/cm');
const rp=path.join(rpRoot,'assets/rlk');
const put=(p,s)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,s.endsWith('\n')?s:s+'\n','utf8');};
const fn=(n,s)=>put(path.join(dp,n+'.mcfunction'),s);
const json=(p,o)=>put(p,JSON.stringify(o,null,2));
const parts=['head','body','right_arm','left_arm','right_leg','left_leg','sword'];
const UV=(a)=>a.map(x=>x/4);
// Box UV layout for a 64x64 player atlas. North is the skin's front face.
function faces(u,v,w,h,d,tex='#skin',sheetHeight=64){
  const face=(x1,y1,x2,y2)=>({uv:[x1/4,y1*16/sheetHeight,x2/4,y2*16/sheetHeight],texture:tex,tintindex:0});
  return {east:face(u,v+d,u+d,v+d+h),north:face(u+d,v+d,u+d+w,v+d+h),west:face(u+d+w,v+d,u+2*d+w,v+d+h),south:face(u+2*d+w,v+d,u+2*d+2*w,v+d+h),up:face(u+d,v,u+d+w,v+d),down:face(u+d+w,v+d,u+d+2*w,v)};
}
const box=(from,to,uv,inflate=0,tex='#skin',sheetHeight=64)=>({from:from.map(x=>x-inflate),to:to.map(x=>x+inflate),faces:faces(...uv,tex,sheetHeight)});
const shapes={
 head:{from:[4,8,4],to:[12,16,12],uv:[0,0,8,8,8],over:[32,0,8,8,8],inflate:.5},
 body:{from:[4,-4,6],to:[12,8,10],uv:[16,16,8,12,4],over:[16,32,8,12,4],inflate:.25},
 right_arm:{from:[6,-2,6],to:[10,10,10],uv:[40,16,4,12,4],over:[40,32,4,12,4],inflate:.25},
 left_arm:{from:[6,-2,6],to:[10,10,10],uv:[32,48,4,12,4],over:[48,48,4,12,4],inflate:.25},
 right_leg:{from:[6,-4,6],to:[10,8,10],uv:[0,16,4,12,4],over:[0,32,4,12,4],inflate:.25},
 left_leg:{from:[6,-4,6],to:[10,8,10],uv:[16,48,4,12,4],over:[0,48,4,12,4],inflate:.25}
};
for(const [name,s] of Object.entries(shapes)){
 const model={ambientocclusion:false,textures:{skin:'rlk:skin/mob_sw',particle:'rlk:skin/mob_sw'},elements:[box(s.from,s.to,s.uv),box(s.from,s.to,s.over,s.inflate)]};
 // Original open-face iron cap; stable block sprite avoids versioned armor atlases.
 if(name==='head'){
  model.textures.helmet='rlk:cm/sw/iron_block';
  model.elements.push(
   solid([3,14,3],[13,17,13],'helmet',[4,4,12,12]),
   solid([3,8,12],[13,14,13],'helmet',[4,4,12,12]),
   solid([3,8,3],[4,14,12],'helmet',[4,4,12,12]),
   solid([12,8,3],[13,14,12],'helmet',[4,4,12,12]),
   solid([4,13,3],[12,14,4],'helmet',[4,4,12,12]),
   solid([7.6,10,3],[8.4,13,4],'helmet',[4,4,12,12])
  );
 }
 json(path.join(rp,'models/item/cm/sw',name+'.json'),model);
}
// Original 3D short sword: narrow iron blade, stepped point, crossguard, wrapped grip.
function solid(from,to,tex,uv=[0,0,16,16]){return {from,to,faces:Object.fromEntries(['north','south','east','west','up','down'].map(f=>[f,{texture:'#'+tex,uv,tintindex:0}]))};}
json(path.join(rp,'models/item/cm/sw/sword.json'),{ambientocclusion:false,textures:{metal:'rlk:cm/sw/iron_block',dark:'rlk:cm/sw/polished_deepslate',grip:'rlk:cm/sw/dark_oak_planks',particle:'rlk:cm/sw/iron_block'},elements:[
 solid([7.35,5.8,7.35],[8.65,9.8,8.65],'grip'),solid([7,5.2,7],[9,6.1,9],'dark'),
 solid([4.7,9.3,7.15],[11.3,10.2,8.85],'dark'),solid([6.8,10.2,7.6],[9.2,21.8,8.4],'metal'),
 solid([7.2,21.8,7.6],[8.8,23.1,8.4],'metal'),solid([7.6,23.1,7.6],[8.4,24,8.4],'metal')
]});
for(const p of parts) json(path.join(rp,'items/cm/sw',p+'.json'),{model:{type:'minecraft:model',model:'rlk:item/cm/sw/'+p,tints:[{type:'minecraft:custom_model_data',index:0,default:16777215}]}});

// Block models must keep their vanilla sprites in the block atlas. Register
// distinct item-atlas aliases for the same PNGs instead of stealing their IDs.
const atlasPath=path.join(rpRoot,'assets/minecraft/atlases/items.json');
const atlas=fs.existsSync(atlasPath)?JSON.parse(fs.readFileSync(atlasPath,'utf8')):{sources:[]};
for(const block of ['iron_block','polished_deepslate','dark_oak_planks']){
 const resource='minecraft:block/'+block,sprite='rlk:cm/sw/'+block;
 atlas.sources=atlas.sources.filter(s=>!(s.type==='minecraft:single'&&((s.resource===resource&&(!s.sprite||s.sprite===resource))||s.sprite===sprite)));
 atlas.sources.push({type:'minecraft:single',resource,sprite});
}
if(!atlas.sources.some(s=>s.type==='minecraft:single'&&s.resource==='rlk:skin/mob_sw'))atlas.sources.push({type:'minecraft:single',resource:'rlk:skin/mob_sw'});
json(atlasPath,atlas);

// Pose construction: skin units are 1/16 block, item-model pivot [8,8,8].
// Authored poses use -Z forward and keep the right hand on negative X.
// item_display turns model geometry Y180 AFTER the NBT transformation, so
// runtime motion must use +Z forward without exchanging the left/right limbs.
const rad=x=>x*Math.PI/180;
function mul(a,b){const[x,y,z,w]=a,[X,Y,Z,W]=b;return[w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W,w*W-x*X-y*Y-z*Z];}
function q(e=[0,0,0]){const[x,y,z]=e.map(a=>rad(a)/2);return mul(mul([0,0,Math.sin(z),Math.cos(z)],[0,Math.sin(y),0,Math.cos(y)]),[Math.sin(x),0,0,Math.cos(x)]);}
function rot(a,v){return mul(mul(a,[...v,0]),[-a[0],-a[1],-a[2],a[3]]).slice(0,3);}
const add=(a,b)=>a.map((v,i)=>v+b[i]);
const guard={torso:[4,-8,0],head:[-3,8,0],right_arm:[62,-12,-8],left_arm:[14,0,12],right_leg:[-5,0,-3],left_leg:[6,0,3],weapon:[-98,5,-4]};
function rig(over={}){
 const p={...guard,...over};
 const hip=add([0,.75,0],p.shift||[0,0,0]);
 const t=q(p.torso),root=q(p.root||[0,0,0]);
 const result={};
 const shoulder=add(hip,rot(t,[0,.75,0]));
 result.body={t:shoulder,q:t};
 result.head={t:shoulder,q:mul(t,q(p.head))};
 for(const [name,sign] of [['right_arm',-1],['left_arm',1]]){
  // Open the sword arm 28 degrees toward its own side, around the shoulder.
  // Compose before the authored pose so the complete swing and grip follow it.
  const joint=mul(q([0,name==='right_arm'?28:0,0]),q(p[name]));
  result[name]={t:add(hip,rot(t,[sign*.375,.625,0])),q:mul(t,joint)};
 }
 for(const [name,sign] of [['right_leg',-1],['left_leg',1]]) result[name]={t:add(hip,[sign*.125,0,0]),q:q(p[name])};
 const arm=result.right_arm;
 result.sword={t:add(arm.t,rot(arm.q,[0,-.535,-.015])),q:mul(arm.q,q(p.weapon))};
 for(const a of Object.values(result)){
  a.t=add(p.rootShift||[0,0,0],rot(root,a.t).map(v=>v*(p.size??1)));
  a.q=mul(root,a.q);a.s=[p.size??1,p.size??1,p.size??1];
  // Change forward axis for the complete joint transform, including the sword
  // grip position. F=diag(1,1,-1): t'=F*t, R'=F*R*F. Keep scale positive.
  a.t=[a.t[0],a.t[1],-a.t[2]];
  a.q=[-a.q[0],-a.q[1],a.q[2],a.q[3]];
 }
 // Turn the blade 90 degrees around its local grip-to-tip (Y) axis.
 // Postmultiply in runtime space so the wrist position and blade direction stay fixed.
 result.sword.q=mul(result.sword.q,q([0,90,0]));
 return result;
}
const fl=n=>{const v=Math.abs(n)<.0000005?0:Number(n.toFixed(6));return String(v)+'f';};
const arr=a=>'['+a.map(fl).join(',')+']';
const poses=[];
function pose(id,name,duration,over){
 const r=rig(over);poses.push({id,name,duration,rig:r});
 fn('sw/rig/pose/'+id,`# Original pose ${name}; ${duration}-tick client interpolation.\n`+parts.map(p=>`data merge entity @e[tag=rlk_sw_this,tag=rlk_sw_${p},limit=1] {start_interpolation:0,interpolation_duration:${duration},transformation:{translation:${arr(r[p].t)},left_rotation:${arr(r[p].q)},scale:${arr(r[p].s)},right_rotation:[0f,0f,0f,1f]}}`).join('\n'));
}
// Soft asymmetric breathing, never a copied vanilla animation.
for(let i=0;i<4;i++){const a=i*Math.PI/2;pose(i,'guard_breath_'+i,12,{shift:[0,Math.sin(a)*.012,0],torso:[4+Math.sin(a)*1.3,-8,Math.cos(a)*.5],head:[-3-Math.sin(a),8,0],right_arm:[62+Math.sin(a)*1.8,-12,-8]});}
// A guarded advance, with heel lift and a counter-swinging free arm.
for(let i=0;i<8;i++){const a=i*Math.PI/4,s=Math.sin(a);pose(10+i,'guarded_walk_'+i,3,{shift:[0,Math.abs(Math.cos(a))*.025,0],torso:[7,-8+s*3,-s*1.5],head:[-5,8-s*3,0],right_arm:[61-s*4,-12,-8],left_arm:[14-s*20,0,10],right_leg:[s*29,0,-2],left_leg:[-s*29,0,2]});}
pose(20,'draw_back',3,{shift:[0,-.055,.01],torso:[8,16,-5],head:[-3,-16,2],right_arm:[94,6,-25],left_arm:[32,5,20],right_leg:[-10,0,-7],left_leg:[17,0,7]});
pose(21,'raise_blade',3,{shift:[0,-.07,.025],torso:[-5,29,-9],head:[7,-29,4],right_arm:[139,12,-32],left_arm:[42,-12,28],right_leg:[-13,0,-8],left_leg:[21,0,8],weapon:[-100,0,-8]});
pose(22,'loaded_shoulder',3,{shift:[0,-.04,.02],torso:[-8,32,-8],head:[8,-32,3],right_arm:[155,10,-29],left_arm:[46,-14,26],right_leg:[-12,0,-6],left_leg:[17,0,6],weapon:[-105,0,-6]});
pose(23,'release_anticipation',1,{shift:[0,-.025,-.01],torso:[-1,23,-5],head:[2,-23,1],right_arm:[145,-1,-23],left_arm:[38,-8,24],right_leg:[-17,0,-4],left_leg:[19,0,4],weapon:[-102,0,-6]});
// This target starts at cmT=2 and is reached at cmT=0: the unchanged damage tick.
pose(24,'blade_contact',2,{shift:[0,-.065,-.055],torso:[17,-18,7],head:[-14,18,-4],right_arm:[15,-35,32],left_arm:[13,15,23],right_leg:[21,0,-5],left_leg:[-14,0,5],weapon:[-95,-8,-8]});
pose(30,'cut_follow_through',2,{shift:[0,-.08,-.07],torso:[20,-29,10],head:[-17,29,-5],right_arm:[-20,-43,40],left_arm:[8,13,20],right_leg:[22,0,-5],left_leg:[-15,0,5],weapon:[-97,-8,-12]});
pose(31,'finish_low',3,{shift:[0,-.075,-.055],torso:[13,-22,7],head:[-11,22,-3],right_arm:[-15,-36,32],left_arm:[10,10,17],right_leg:[17,0,-4],left_leg:[-11,0,4],weapon:[-97,-5,-10]});
pose(32,'recover_guard',3,{shift:[0,-.035,-.025],torso:[8,-13,3],head:[-6,13,-2],right_arm:[40,-22,8],left_arm:[14,5,15],right_leg:[7,0,-3],left_leg:[-2,0,3]});
pose(33,'settle_guard',2,guard);
pose(40,'hit_recoil',2,{shift:[0,-.07,.04],torso:[-13,7,-8],head:[14,-7,5],right_arm:[43,4,-25],left_arm:[39,-14,25],right_leg:[-10,0,-5],left_leg:[15,0,5]});
pose(41,'hit_recover',3,{shift:[0,-.035,.02],torso:[-3,-2,-3],head:[5,2,2],right_arm:[52,-5,-17],left_arm:[24,-6,18],right_leg:[-8,0,-4],left_leg:[11,0,4]});
pose(50,'death_buckle',2,{shift:[0,-.19,0],torso:[21,8,-16],head:[18,-8,-9],right_arm:[29,5,-30],left_arm:[45,10,30],right_leg:[-23,0,-13],left_leg:[34,0,13]});
pose(51,'death_fall',4,{root:[4,0,-52],rootShift:[0,.20,0],shift:[0,-.06,0],torso:[7,3,-8],head:[14,3,6],right_arm:[7,0,-10],left_arm:[22,5,24],right_leg:[-9,0,-4],left_leg:[19,0,5]});
pose(52,'death_land',3,{root:[0,0,-88],rootShift:[0,.30,0],torso:[5,0,0],head:[12,8,4],right_arm:[4,0,-10],left_arm:[26,8,25],right_leg:[-7,0,0],left_leg:[16,0,3]});
pose(53,'death_dissolve',4,{root:[0,0,-88],rootShift:[0,.10,0],torso:[5,0,0],head:[12,8,4],right_arm:[4,0,-10],left_arm:[26,8,25],right_leg:[-7,0,0],left_leg:[16,0,3],size:.04});
fn('sw/rig/apply',poses.filter(p=>p.id<50).map(p=>`execute if score #swPose tmp matches ${p.id} run function rlk:cm/sw/rig/pose/${p.id}`).join('\n'));
json(path.join(base,'swordsman_poses.json'),{authoring:'Original keyframes authored for roguelike; 20 ticks/second; no reference motions copied.',space:'Runtime item_display transformations: +Z forward, right hand on -X. Apply the renderer Y180 to model geometry after these transforms.',parts,poses});

fn('sw/rig/select',`# @s = owning husk or corpse anchor. cmId is the sole ownership key.
tag @e[tag=rlk_sw_this] remove rlk_sw_this
scoreboard players operation #swId tmp = @s cmId
execute as @e[tag=rlk_sw_rig] if score @s cmId = #swId tmp run tag @s add rlk_sw_this`);
fn('sw/rig/rebuild',`# Reload migration / repair: only this swordsman's visuals are replaced.
function rlk:cm/sw/rig/select
kill @e[tag=rlk_sw_this]
execute as @e[tag=rlk_cmv] if score @s cmId = #swId tmp run kill @s
scoreboard players set @s cmAF 0
scoreboard players set @s cmAH 0
scoreboard players set @s cmAR 0
scoreboard players set @s cmAP -1
execute store result score @s cmAX run data get entity @s Pos[0] 1000
execute store result score @s cmAZ run data get entity @s Pos[2] 1000
function rlk:cm/sw/rig/create`);
let spawn=`# Seven displays plus a feet-origin anchor. Geometry pivot is [8,8,8].\n`;
spawn+=`summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_sw_rig","rlk_sw_anchor","rlk_cmlink","rlk_cmsync","rlk_sw_new"]}\n`;
for(const p of parts)spawn+=`summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_pet","rlk_sw_rig","rlk_sw_part","rlk_sw_${p}","rlk_cmlink","rlk_cmsync","rlk_sw_new"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:1.5f,width:3.6f,height:3.6f,shadow_radius:0f,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:cm/sw/${p}","minecraft:custom_model_data":{colors:[16777215]}}}}\n`;
spawn+=`scoreboard players operation @e[tag=rlk_sw_new] cmId = #swId tmp
tag @e[tag=rlk_sw_new] add rlk_sw_this
tag @e[tag=rlk_sw_new] remove rlk_sw_new
scoreboard players set @e[tag=rlk_sw_this,tag=rlk_sw_anchor] cmAD 0
function rlk:cm/sw/rig/pose/0
tag @e[tag=rlk_sw_this] remove rlk_sw_this`;
fn('sw/rig/create',spawn);
fn('sw/rig/hurt',`# Called at the existing confirmed-damage event, before the gameplay health check.
scoreboard players set @s cmAH 6
function rlk:cm/sw/rig/select
execute as @e[tag=rlk_sw_this,tag=rlk_sw_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16737903]}
tag @e[tag=rlk_sw_this] remove rlk_sw_this`);
fn('sw/rig/tick',`# @s = invisible swordsman husk, at @s. Actual AI and damage remain in cm/sw.
function rlk:cm/sw/rig/select
execute store result score #swCount tmp if entity @e[tag=rlk_sw_this]
execute unless score #swCount tmp matches 8 run function rlk:cm/sw/rig/rebuild
execute unless score #swCount tmp matches 8 run function rlk:cm/sw/rig/select
tag @e[tag=rlk_sw_this] add rlk_cmsync
# The anchor and all joints share the same feet origin and yaw; never copy camera pitch.
execute facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 as @e[tag=rlk_sw_this] run tp @s ~ ~ ~ ~ 0
execute store result score #swX tmp run data get entity @s Pos[0] 1000
execute store result score #swZ tmp run data get entity @s Pos[2] 1000
scoreboard players operation #swDX tmp = #swX tmp
scoreboard players operation #swDZ tmp = #swZ tmp
scoreboard players operation #swDX tmp -= @s cmAX
scoreboard players operation #swDZ tmp -= @s cmAZ
scoreboard players set #swNeg tmp -1
execute if score #swDX tmp matches ..-1 run scoreboard players operation #swDX tmp *= #swNeg tmp
execute if score #swDZ tmp matches ..-1 run scoreboard players operation #swDZ tmp *= #swNeg tmp
scoreboard players operation #swMove tmp = #swDX tmp
scoreboard players operation #swMove tmp += #swDZ tmp
scoreboard players operation @s cmAX = #swX tmp
scoreboard players operation @s cmAZ = #swZ tmp
execute if score @s cmAH matches 1 as @e[tag=rlk_sw_this,tag=rlk_sw_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
# Freeze preserves the current client pose and pauses the visual timers.
execute if score @s frzT matches 1.. run return run function rlk:cm/sw/rig/frozen
scoreboard players add @s cmAF 1
execute if score @s cmAF matches 48.. run scoreboard players set @s cmAF 0
scoreboard players operation #swFrame tmp = @s cmAF
scoreboard players set #swDiv tmp 12
scoreboard players operation #swFrame tmp /= #swDiv tmp
scoreboard players operation #swPose tmp = #swFrame tmp
execute if score #swMove tmp matches 8.. run function rlk:cm/sw/rig/walk
# Recovery is visual only; the original AI/cooldown/attack range are unchanged.
execute if score @s cmAR matches 9.. run scoreboard players set #swPose tmp 30
execute if score @s cmAR matches 6..8 run scoreboard players set #swPose tmp 31
execute if score @s cmAR matches 3..5 run scoreboard players set #swPose tmp 32
execute if score @s cmAR matches 1..2 run scoreboard players set #swPose tmp 33
execute if score @s cmS matches 1 run function rlk:cm/sw/rig/wind
execute if score @s cmAH matches 4.. run scoreboard players set #swPose tmp 40
execute if score @s cmAH matches 1..3 run scoreboard players set #swPose tmp 41
execute unless score @s cmAP = #swPose tmp run function rlk:cm/sw/rig/apply
scoreboard players operation @s cmAP = #swPose tmp
execute if score @s cmAR matches 1.. run scoreboard players remove @s cmAR 1
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_sw_this] remove rlk_sw_this`);
fn('sw/rig/walk',`scoreboard players operation #swFrame tmp = @s cmAF
scoreboard players set #swDiv tmp 24
scoreboard players operation #swFrame tmp %= #swDiv tmp
scoreboard players set #swDiv tmp 3
scoreboard players operation #swFrame tmp /= #swDiv tmp
scoreboard players operation #swPose tmp = #swFrame tmp
scoreboard players add #swPose tmp 10`);
fn('sw/rig/frozen',`# Leave joint rotations still while clearing the brief damage flash normally.
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_sw_this] remove rlk_sw_this`);
fn('sw/rig/wind',`# Normalize anticipation to the configured windup; last two ticks always approach contact.
scoreboard players operation #swWind tmp = @s cmT
scoreboard players remove #swWind tmp 4
scoreboard players set #swThree tmp 3
scoreboard players operation #swWind tmp *= #swThree tmp
scoreboard players operation #swDiv tmp = #cmW_sw tmp
scoreboard players remove #swDiv tmp 3
execute if score #swDiv tmp matches ..0 run scoreboard players set #swDiv tmp 1
scoreboard players operation #swWind tmp /= #swDiv tmp
scoreboard players set #swPose tmp 22
execute if score #swWind tmp matches 2.. run scoreboard players set #swPose tmp 20
execute if score #swWind tmp matches 1 run scoreboard players set #swPose tmp 21
execute if score @s cmT matches 3 run scoreboard players set #swPose tmp 23
execute if score @s cmT matches 1..2 run scoreboard players set #swPose tmp 24`);
fn('sw/rig/die',`# Missing owner: transfer the rig to a short-lived visual corpse, by cmId.
function rlk:cm/sw/rig/select
tag @e[tag=rlk_sw_this] add rlk_sw_dying
scoreboard players set @s cmAD 0
execute as @e[tag=rlk_sw_this,tag=rlk_sw_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
function rlk:cm/sw/rig/pose/50
tag @e[tag=rlk_sw_this] remove rlk_sw_this`);
fn('sw/rig/death_tick',`function rlk:cm/sw/rig/select
scoreboard players add @s cmAD 1
execute if score @s cmAD matches 3 run function rlk:cm/sw/rig/pose/51
execute if score @s cmAD matches 7 run function rlk:cm/sw/rig/pose/52
execute if score @s cmAD matches 10 run function rlk:cm/sw/rig/pose/53
execute if score @s cmAD matches 14.. run kill @e[tag=rlk_sw_this]
tag @e[tag=rlk_sw_this] remove rlk_sw_this`);

// Narrow, repeatable edits to shared cm hooks.
function insertOnce(n,anchor,extra){const p=path.join(dp,n+'.mcfunction');let s=fs.readFileSync(p,'utf8').replace(/\r\n/g,'\n');if(!s.includes(extra)){if(!s.includes(anchor))throw Error('Missing patch anchor '+n);s=s.replace(anchor,anchor+'\n'+extra);put(p,s);}}
function prefixOnce(n,extra){const p=path.join(dp,n+'.mcfunction');let s=fs.readFileSync(p,'utf8').replace(/\r\n/g,'\n');if(!s.includes(extra))put(p,extra+'\n'+s);}
let oldSpawn=fs.readFileSync(path.join(dp,'spawn/sw.mcfunction'),'utf8').replace(/\r\n/g,'\n');
oldSpawn=oldSpawn.split('\n').filter(l=>!l.includes('minecraft:mannequin')&&!l.includes('rlk_cmvnew')).join('\n').replace('# 커스텀 몹 소환(실행 위치): 두뇌(투명 허스크) + 모습(마네킹)','# 검사: 기존 투명 허스크 두뇌 + cmId로 연결한 원본 디스플레이 리그');
put(path.join(dp,'spawn/sw.mcfunction'),oldSpawn);
insertOnce('init','execute if entity @s[tag=rlk_cm_cn] run function rlk:cm/cn/build','execute if entity @s[tag=rlk_cm_sw] run function rlk:cm/sw/rig/rebuild');
prefixOnce('vis','execute if entity @s[tag=rlk_cm_sw] run return run function rlk:cm/sw/rig/tick');
prefixOnce('flash','execute if entity @s[tag=rlk_cm_sw] run return run function rlk:cm/sw/rig/hurt');
insertOnce('sw/strike','scoreboard players set @s cmS 0','scoreboard players set @s cmAR 11');
insertOnce('sw/start','scoreboard players set @s cmS 1','scoreboard players set @s cmAR 0');
insertOnce('cancel','scoreboard players set @s cmS 0','execute if entity @s[tag=rlk_cm_sw] run scoreboard players set @s cmAR 0');
const cp=path.join(dp,'clean.mcfunction');let clean=fs.readFileSync(cp,'utf8').replace(/\r\n/g,'\n');
const cleanHead='execute as @e[tag=rlk_sw_anchor,tag=!rlk_cmsync,tag=!rlk_sw_dying] at @s run function rlk:cm/sw/rig/die\nexecute as @e[tag=rlk_sw_anchor,tag=rlk_sw_dying] at @s run function rlk:cm/sw/rig/death_tick';
if(!clean.includes('rlk:cm/sw/rig/die'))clean=cleanHead+'\n'+clean;
clean=clean.replace('kill @e[tag=rlk_cmlink,tag=!rlk_cmsync]','kill @e[tag=rlk_cmlink,tag=!rlk_cmsync,tag=!rlk_sw_dying]');put(cp,clean);
console.log(JSON.stringify({models:parts.length,itemDefinitions:parts.length,originalPoses:poses.length,objectives:['cmAF','cmAH','cmAR','cmAX','cmAZ','cmAP','cmAD']},null,2));
