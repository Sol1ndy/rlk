// Original cannon/operator rig. All shapes and keyframes authored for this pack.
// node tools/build_cannon.mjs --datapack <pack> --resourcepack <unpacked pack>
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const arg=n=>process.argv[process.argv.indexOf(n)+1];
const dp=path.resolve(arg('--datapack')),rp=path.resolve(arg('--resourcepack'));
if(!fs.existsSync(path.join(dp,'pack.mcmeta'))||!fs.existsSync(path.join(rp,'pack.mcmeta')))throw Error('Both pack roots are required.');
const put=(p,s)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,s.endsWith('\n')?s:s+'\n');};
const fn=(n,s)=>put(path.join(dp,'data/rlk/function/cm/cn',n+'.mcfunction'),s);
const json=(p,v)=>put(p,JSON.stringify(v,null,2));
const parts=['head','body','right_arm','left_arm','right_leg','left_leg','carriage','barrel','fuse','flint'];
function faces(u,v,w,h,d){const f=(a,b,c,e)=>({uv:[a/4,b/4,c/4,e/4],texture:'#skin',tintindex:0});return{east:f(u,v+d,u+d,v+d+h),north:f(u+d,v+d,u+d+w,v+d+h),west:f(u+d+w,v+d,u+2*d+w,v+d+h),south:f(u+2*d+w,v+d,u+2*d+2*w,v+d+h),up:f(u+d,v,u+d+w,v+d),down:f(u+d+w,v+d,u+d+2*w,v)};}
function skinBox(s,over=false){const k=over?s.inflate:0;return{from:s.from.map(x=>x-k),to:s.to.map(x=>x+k),faces:faces(...(over?s.over:s.uv))};}
const shapes={head:{from:[4,8,4],to:[12,16,12],uv:[0,0,8,8,8],over:[32,0,8,8,8],inflate:.5},body:{from:[4,-4,6],to:[12,8,10],uv:[16,16,8,12,4],over:[16,32,8,12,4],inflate:.25},right_arm:{from:[6,-2,6],to:[10,10,10],uv:[40,16,4,12,4],over:[40,32,4,12,4],inflate:.25},left_arm:{from:[6,-2,6],to:[10,10,10],uv:[32,48,4,12,4],over:[48,48,4,12,4],inflate:.25},right_leg:{from:[6,-4,6],to:[10,8,10],uv:[0,16,4,12,4],over:[0,32,4,12,4],inflate:.25},left_leg:{from:[6,-4,6],to:[10,8,10],uv:[16,48,4,12,4],over:[0,48,4,12,4],inflate:.25}};
for(const[n,s]of Object.entries(shapes))json(path.join(rp,'assets/rlk/models/item/cm/cn',n+'.json'),{ambientocclusion:false,textures:{skin:'rlk:skin/mob_cn',particle:'rlk:skin/mob_cn'},elements:[skinBox(s),skinBox(s,true)]});
const solid=(a,b,t)=>({from:a,to:b,faces:Object.fromEntries(['north','south','east','west','up','down'].map(f=>[f,{texture:'#'+t,uv:[0,0,16,16],tintindex:0}]))});
const textures={wood:'rlk:cm/cn/dark_oak_planks',metal:'rlk:cm/cn/iron_block',dark:'rlk:cm/cn/polished_blackstone',rope:'rlk:cm/cn/stripped_spruce_log',fire:'rlk:cm/cn/orange_concrete',particle:'rlk:cm/cn/polished_blackstone'};
const carriage=[solid([.5,9,-1],[15.5,12,20],'wood'),solid([5.5,7,16],[10.5,10,25],'wood'),solid([-4,12,4],[20,14,6],'metal')];
for(const x of[-5,17]){carriage.push(solid([x,8,1],[x+4,20,9],'wood'),solid([x,10,-1],[x+4,18,11],'wood'),solid([x,7,3],[x+4,21,7],'wood'),solid([x-.25,12,3],[x+4.25,16,7],'metal'));}
json(path.join(rp,'assets/rlk/models/item/cm/cn/carriage.json'),{ambientocclusion:false,textures,elements:carriage});
// The new barrel is 1.90 blocks long and 0.60 wide (old barrel: 1.25 x 0.34).
const barrel=[solid([4,5,-9],[12,11,21],'dark'),solid([3.3,6,-9],[12.7,10,21],'dark'),solid([5,4.3,-9],[11,11.7,21],'dark'),solid([4.5,5.5,21],[11.5,10.5,23],'metal')];
for(const z of[-8.9,3.5,16]){barrel.push(solid([3,3.8,z],[13,5,z+1.8],'metal'),solid([3,11,z],[13,12.2,z+1.8],'metal'),solid([3,5,z],[4,11,z+1.8],'metal'),solid([12,5,z],[13,11,z+1.8],'metal'));}
// Recessed dark mouth gives the enlarged barrel a visible opening.
barrel.push(solid([4.25,5.1,-9.05],[11.75,10.9,-8.9],'dark'));
json(path.join(rp,'assets/rlk/models/item/cm/cn/barrel.json'),{ambientocclusion:false,textures,elements:barrel});
json(path.join(rp,'assets/rlk/models/item/cm/cn/fuse.json'),{ambientocclusion:false,textures,elements:[solid([7.4,7.2,7.4],[8.6,11.6,8.6],'rope'),solid([7.15,11.4,7.15],[8.85,12.4,8.85],'dark')]});
json(path.join(rp,'assets/rlk/models/item/cm/cn/flint.json'),{ambientocclusion:false,textures,elements:[solid([6.7,6.8,7.4],[9.3,9.2,8.6],'dark'),solid([6.2,7.6,7.2],[6.9,10.5,8.8],'metal')]});
for(const part of parts)json(path.join(rp,'assets/rlk/items/cm/cn',part+'.json'),{model:{type:'minecraft:model',model:'rlk:item/cm/cn/'+part,tints:[{type:'minecraft:custom_model_data',index:0,default:16777215}]}});
// Atlas aliases are installed by the shared pack integration; never steal a vanilla block sprite.
const rad=x=>x*Math.PI/180;
const mul=(a,b)=>{const[x,y,z,w]=a,[X,Y,Z,W]=b;return[w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W,w*W-x*X-y*Y-z*Z];};
const q=(e=[0,0,0])=>{const[x,y,z]=e.map(n=>rad(n)/2);return mul(mul([0,0,Math.sin(z),Math.cos(z)],[0,Math.sin(y),0,Math.cos(y)]),[Math.sin(x),0,0,Math.cos(x)]);};
const rot=(a,v)=>mul(mul(a,[...v,0]),[-a[0],-a[1],-a[2],a[3]]).slice(0,3);
const add=(a,b)=>a.map((x,i)=>x+b[i]);
const base={torso:[-16,0,0],head:[17,0,0],right_arm:[104,-10,-8],left_arm:[104,10,8],right_leg:[-7,0,-5],left_leg:[6,0,5],humanShift:[0,0,.82]};
function rig(over={}){
 const p={...base,...over},out={},hip=add([0,.75,0],p.shift||[0,0,0]),t=q(p.torso),shoulder=add(hip,rot(t,[0,.75,0]));
 out.body={t:shoulder,q:t};out.head={t:shoulder,q:mul(t,q(p.head))};
 for(const[n,s]of[['right_arm',-1],['left_arm',1]])out[n]={t:add(hip,rot(t,[s*.375,.625,0])),q:mul(t,q(p[n]))};
 for(const[n,s]of[['right_leg',-1],['left_leg',1]])out[n]={t:add(hip,[s*.125,0,0]),q:q(p[n])};
 const arm=out.right_arm;out.flint={t:add(arm.t,rot(arm.q,[0,-.56,0])),q:mul(arm.q,q([0,25,0])),s:[.72,.72,.72]};
 const root=q(p.humanRoot||[0,0,0]);
 for(const value of Object.values(out)){value.t=add(p.humanShift,rot(root,value.t).map(x=>x*.9));value.q=mul(root,value.q);value.s=(value.s||[1,1,1]).map(x=>x*.9);}
 if(!p.flint)out.flint.s=[0,0,0];
 out.carriage={t:[0,.0875,p.recoil||0],q:q(),s:[1,1,1]};
 out.barrel={t:[0,.99,-.25+(p.recoil||0)+(p.barrelBack||0)],q:q([p.barrelPitch??6,0,0]),s:p.barrelScale||[1,1,1]};
 out.fuse={t:[0,1.22,.55+(p.recoil||0)+(p.barrelBack||0)],q:q([-22,0,0]),s:p.fuse===false?[0,0,0]:[1,1,1]};
 for(const v of Object.values(out)){const size=p.size??1;v.t=v.t.map(x=>x*size);v.s=v.s.map(x=>x*size);v.t=[v.t[0],v.t[1],-v.t[2]];v.q=[-v.q[0],-v.q[1],v.q[2],v.q[3]];}
 return out;
}
const fl=x=>(Math.abs(x)<.0000005?'0':String(Number(x.toFixed(6))))+'f',arr=a=>'['+a.map(fl).join(',')+']',poses=[];
function pose(id,name,duration,over){const r=rig(over);poses.push({id,name,duration,rig:r});fn('rig/pose/'+id,`# Original cannon pose: ${name}\n`+parts.map(n=>`data merge entity @e[tag=rlk_cn_this,tag=rlk_cn_${n},limit=1] {start_interpolation:0,interpolation_duration:${duration},transformation:{translation:${arr(r[n].t)},left_rotation:${arr(r[n].q)},scale:${arr(r[n].s)},right_rotation:[0f,0f,0f,1f]}}`).join('\n'));}
for(let i=0;i<4;i++){const s=Math.sin(i*Math.PI/2);pose(i,'lean_on_breech_'+i,12,{torso:[-16+s,0,0],head:[17-s,0,0],shift:[0,s*.008,0]});}
pose(10,'retrieve_striker',4,{torso:[-8,14,-3],head:[12,-14,0],right_arm:[15,-18,-17],left_arm:[102,10,8],flint:true});
pose(11,'bring_striker_to_fuse',4,{torso:[-13,8,-4],head:[23,-9,0],right_arm:[145,-45,-30],humanShift:[0,0,.97],flint:true});
pose(12,'strike_fuse',2,{torso:[-19,4,-2],head:[28,-4,0],right_arm:[155,-45,-30],humanShift:[0,0,.97],flint:true});
pose(13,'lift_after_ignition',3,{torso:[-9,-4,3],head:[15,4,-3],right_arm:[168,-50,-35],left_arm:[102,9,8],humanShift:[0,0,.95],flint:true});
pose(14,'take_cover',4,{torso:[-4,-11,2],head:[5,11,0],right_arm:[42,-15,-25],left_arm:[55,20,22],shift:[0,-.045,0],humanShift:[0,0,.88],fuse:false});
pose(20,'brace_for_fire',3,{torso:[-12,0,0],head:[15,0,0],right_arm:[53,-18,-14],left_arm:[67,18,14],shift:[0,-.08,0],humanShift:[0,0,.9],fuse:false});
pose(30,'shot_squash',1,{torso:[6,0,-4],head:[-2,0,2],right_arm:[97,-10,-24],left_arm:[104,14,24],shift:[0,-.07,0],humanShift:[0,0,.96],recoil:.1,barrelBack:.13,barrelScale:[1.12,1.1,.78],barrelPitch:3,fuse:false});
pose(31,'barrel_rebound',2,{torso:[-5,0,-2],head:[9,0,0],right_arm:[82,-10,-17],left_arm:[84,14,19],shift:[0,-.055,0],humanShift:[0,0,.9],recoil:.06,barrelBack:.07,barrelScale:[.96,.97,1.05],barrelPitch:9,fuse:false});
pose(32,'barrel_settle',3,{torso:[-14,0,0],head:[16,0,0],right_arm:[76,-10,-12],left_arm:[77,12,12],recoil:.025,barrelBack:.025,barrelScale:[1.02,1.015,.98],fuse:false});
pose(33,'hands_back_on_cannon',4,{fuse:false});
pose(50,'operator_falls_back',3,{torso:[18,7,-14],head:[20,-7,0],right_arm:[45,-10,-26],left_arm:[60,17,29],shift:[0,-.24,0],humanShift:[0,0,.92],fuse:false});
pose(51,'operator_down',4,{humanRoot:[54,0,-22],humanShift:[0,.35,.55],torso:[10,0,0],head:[12,0,0],right_arm:[13,0,-11],left_arm:[18,0,20],right_leg:[12,0,-8],left_leg:[-9,0,9],barrelPitch:8,fuse:false});
pose(52,'cannon_fade',4,{humanRoot:[54,0,-22],humanShift:[0,.35,.55],size:.03,fuse:false});
json(path.join(here,'cannon_poses.json'),{authoring:'Original cannon animation, 20 ticks per second.',parts,poses,atlas:[{resource:'rlk:skin/mob_cn'},...['dark_oak_planks','iron_block','polished_blackstone','stripped_spruce_log','orange_concrete'].map(n=>({resource:'minecraft:block/'+n,sprite:'rlk:cm/cn/'+n}))]});
fn('rig/apply',poses.filter(p=>p.id<50).map(p=>`execute if score #cnPose tmp matches ${p.id} run function rlk:cm/cn/rig/pose/${p.id}`).join('\n'));
fn('rig/select',`tag @e[tag=rlk_cn_this] remove rlk_cn_this
scoreboard players operation #cnId tmp = @s cmId
execute as @e[tag=rlk_cn_rig] if score @s cmId = #cnId tmp run tag @s add rlk_cn_this`);
fn('rig/rebuild',`# Existing mannequin and old block cannon are replaced only for this cmId.
function rlk:cm/cn/rig/select
kill @e[tag=rlk_cn_this]
execute as @e[tag=rlk_cmv] if score @s cmId = #cnId tmp run kill @s
execute as @e[tag=rlk_cmcan] if score @s cmId = #cnId tmp run kill @s
scoreboard players set @s cmAF 0
scoreboard players set @s cmAH 0
scoreboard players set @s cmAR 0
scoreboard players set @s cmAP -1
function rlk:cm/cn/stabilize
function rlk:cm/cn/rig/create`);
let create='summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_cn_rig","rlk_cn_anchor","rlk_cmlink","rlk_cmsync","rlk_cn_new"]}\n';
for(const p of parts)create+=`summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_pet","rlk_cn_rig","rlk_cn_part","rlk_cn_${p}","rlk_cmlink","rlk_cmsync","rlk_cn_new"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:1.5f,width:4f,height:4f,shadow_radius:0f,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:cm/cn/${p}","minecraft:custom_model_data":{colors:[16777215]}}}}\n`;
create+=`scoreboard players operation @e[tag=rlk_cn_new] cmId = #cnId tmp
tag @e[tag=rlk_cn_new] add rlk_cn_this
tag @e[tag=rlk_cn_new] remove rlk_cn_new
scoreboard players set @e[tag=rlk_cn_this,tag=rlk_cn_anchor] cmAD 0
function rlk:cm/cn/rig/pose/0
tag @e[tag=rlk_cn_this] remove rlk_cn_this`;
fn('rig/create',create);
fn('rig/aim',`function rlk:cm/cn/rig/select
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 as @e[tag=rlk_cn_this] run tp @s ~ ~ ~ ~ 0
tag @e[tag=rlk_cn_this] remove rlk_cn_this`);
fn('rig/hurt',`# Color feedback only: this siege unit never plays a hit-stagger pose.
scoreboard players set @s cmAH 5
function rlk:cm/cn/rig/select
execute as @e[tag=rlk_cn_this,tag=rlk_cn_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16737903]}
tag @e[tag=rlk_cn_this] remove rlk_cn_this`);
fn('rig/tick',`function rlk:cm/cn/rig/select
execute store result score #cnCount tmp if entity @e[tag=rlk_cn_this]
execute unless score #cnCount tmp matches 11 run function rlk:cm/cn/rig/rebuild
execute unless score #cnCount tmp matches 11 run function rlk:cm/cn/rig/select
execute unless score @s cmS matches 2 unless score @s cmAR matches 1.. facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 as @e[tag=rlk_cn_this] run tp @s ~ ~ ~ ~ 0
execute as @e[tag=rlk_cmlink] if score @s cmId = #cnId tmp run tag @s add rlk_cmsync
execute if score @s cmAH matches 1 as @e[tag=rlk_cn_this,tag=rlk_cn_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
execute if score @s frzT matches 1.. run return run function rlk:cm/cn/rig/frozen
scoreboard players add @s cmAF 1
execute if score @s cmAF matches 48.. run scoreboard players set @s cmAF 0
scoreboard players operation #cnPose tmp = @s cmAF
scoreboard players set #cnDiv tmp 12
scoreboard players operation #cnPose tmp /= #cnDiv tmp
execute if score @s cmS matches 1 run function rlk:cm/cn/rig/wind
execute if score @s cmS matches 2 run scoreboard players set #cnPose tmp 20
execute if score @s cmAR matches 10.. run scoreboard players set #cnPose tmp 30
execute if score @s cmAR matches 8..9 run scoreboard players set #cnPose tmp 31
execute if score @s cmAR matches 5..7 run scoreboard players set #cnPose tmp 32
execute if score @s cmAR matches 1..4 run scoreboard players set #cnPose tmp 33
execute unless score @s cmAP = #cnPose tmp run function rlk:cm/cn/rig/apply
scoreboard players operation @s cmAP = #cnPose tmp
execute if score @s cmAR matches 1.. run scoreboard players remove @s cmAR 1
tag @e[tag=rlk_cn_this] remove rlk_cn_this`);
fn('rig/frozen','tag @e[tag=rlk_cn_this] remove rlk_cn_this');
fn('rig/wind',`# Normalize the five anticipation stages to configured fuse duration.
scoreboard players operation #cnWind tmp = @s cmT
scoreboard players set #cnDiv tmp 5
scoreboard players operation #cnWind tmp *= #cnDiv tmp
scoreboard players operation #cnDiv tmp = #cmW_cn tmp
execute if score #cnDiv tmp matches ..0 run scoreboard players set #cnDiv tmp 1
scoreboard players operation #cnWind tmp /= #cnDiv tmp
scoreboard players set #cnPose tmp 14
execute if score #cnWind tmp matches 4.. run scoreboard players set #cnPose tmp 10
execute if score #cnWind tmp matches 3 run scoreboard players set #cnPose tmp 11
execute if score #cnWind tmp matches 2 run scoreboard players set #cnPose tmp 12
execute if score #cnWind tmp matches 1 run scoreboard players set #cnPose tmp 13`);
fn('rig/die',`function rlk:cm/cn/rig/select
tag @e[tag=rlk_cn_this] add rlk_cn_dying
scoreboard players set @s cmAD 0
execute as @e[tag=rlk_cn_this,tag=rlk_cn_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
function rlk:cm/cn/rig/pose/50
tag @e[tag=rlk_cn_this] remove rlk_cn_this`);
fn('rig/death_tick',`function rlk:cm/cn/rig/select
scoreboard players add @s cmAD 1
execute if score @s cmAD matches 4 run function rlk:cm/cn/rig/pose/51
execute if score @s cmAD matches 9 run function rlk:cm/cn/rig/pose/52
execute if score @s cmAD matches 14.. run kill @e[tag=rlk_cn_this]
tag @e[tag=rlk_cn_this] remove rlk_cn_this`);
fn('build','# Backward-compatible entry point used by cm/init.\nfunction rlk:cm/cn/rig/rebuild');
fn('stabilize',`# Stationary siege unit; command knockback is excluded by shared hit handling.
# Clear an old stagger on reload without touching the separate elemental freeze state.
execute if score @s stunT matches 0.. run function rlk:mob/unstun
data merge entity @s {NoAI:1b,Motion:[0d,0d,0d]}
attribute @s minecraft:knockback_resistance base set 1
attribute @s minecraft:explosion_knockback_resistance base set 1
scoreboard players set #hold tmp 1`);
const check=['# Run at the block center. A complete flat 3x3 full-block floor and 3 blocks of clear headroom are mandatory.','scoreboard players set #cnSpawnOk tmp 0'];
check.push('# Keep the three-by-three emplacement separate from nearby artillery.','execute positioned ~-2.5 ~ ~-2.5 if entity @e[tag=rlk_cm_cn,dx=4,dy=2,dz=4] run return 0');
for(let x=-1;x<=1;x++)for(let z=-1;z<=1;z++){const pos=`~${x||''} ~-1 ~${z||''}`;check.push(`execute unless block ${pos} #rlk:cannon_floor run return 0`);for(let y=0;y<3;y++)check.push(`execute unless block ~${x||''} ~${y||''} ~${z||''} #rlk:cannon_clear run return 0`);}
check.push('scoreboard players set #cnSpawnOk tmp 1','return 1');fn('can_spawn',check.join('\n'));
fn('spawn_at',`function rlk:cm/cn/can_spawn
execute unless score #cnSpawnOk tmp matches 1 run return 0
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_cmb","rlk_cm_cn","rlk_m_cmcn","rlk_cmnew"],PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Silent:1b,IsBaby:0b,CanPickUpLoot:0b,NoAI:1b,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b,ambient:1b}]}
scoreboard players add #cmIdC tmp 1
scoreboard players operation @e[tag=rlk_cmnew] cmId = #cmIdC tmp
execute as @e[tag=rlk_cmnew] at @s run function rlk:cm/init
return 1`);
put(path.join(dp,'data/rlk/function/cm/spawn/cn.mcfunction'),`# Spawn only at a centered, flat 3x3 site; never silently substitute a different mob.
execute align xyz positioned ~0.5 ~ ~0.5 run return run function rlk:cm/cn/spawn_at`);
// These gameplay edits are intentionally narrow: timing, trajectory and damage stay original.
fn('tick',`# Cannon remains planted at its validated 3x3 site, including when the target is far away.
function rlk:cm/cn/stabilize
execute if score @s cmS matches 1 run return run function rlk:cm/cn/fuse
execute if score @s cmS matches 2 run return run function rlk:cm/cn/wait
execute if score @s cmCd matches ..0 unless score @s frzT matches 1.. if entity @e[tag=rlk_body,distance=..24] run function rlk:cm/cn/start`);
fn('fuse',`scoreboard players set #hold tmp 1
scoreboard players remove @s cmT 1
# Ignite only after the hand reaches the fuse; smoke is attached to the larger breech.
scoreboard players operation #cnFuse tmp = #cmW_cn tmp
scoreboard players set #cnDiv tmp 5
scoreboard players operation #cnFuse tmp *= #2 tmp
scoreboard players operation #cnFuse tmp /= #cnDiv tmp
execute if score @s cmT <= #cnFuse tmp facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^1.47 ^-0.55 run particle minecraft:smoke ~ ~ ~ 0.025 0.025 0.025 0.01 2
execute if score @s cmT <= #cnFuse tmp facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^1.47 ^-0.55 run particle minecraft:small_flame ~ ~ ~ 0.015 0.02 0.015 0.005 1
execute if score @s cmT matches ..0 run function rlk:cm/cn/fire`);
fn('fire',`# Keep the last aimed yaw throughout the existing delayed shot.
function rlk:cm/cn/rig/aim
scoreboard players set @s cmS 2
scoreboard players operation @s cmT = #cmW_cnD tmp
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^1.12 ^1.30 run function rlk:cm/cn/shot`);
fn('launch',`execute as @e[tag=rlk_cmcbw,distance=..6] if score @s cmId = #cid tmp at @s run function rlk:cm/cn/go
scoreboard players set @s cmS 0
scoreboard players operation @s cmCd = #cmCd_cn tmp
scoreboard players set @s cmAR 10
tag @s remove rlk_cmch
function rlk:cm/swing`);
console.log('Built original cannon/operator model, poses, runtime and flat-site spawn wrapper.');
