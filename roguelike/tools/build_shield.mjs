// Original shield soldier geometry and keyframes for roguelike.
// node tools/build_shield.mjs --datapack <datapack> --resourcepack <unpacked resourcepack>
// Shared cm lifecycle hooks and the item atlas are integrated by the pack maintainer.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const base=path.dirname(fileURLToPath(import.meta.url));
const arg=n=>{const i=process.argv.indexOf(n);return i<0?undefined:process.argv[i+1];};
const dpRoot=path.resolve(arg('--datapack')||path.join(base,'..'));
if(!arg('--resourcepack'))throw new Error('Provide --resourcepack.');
const rpRoot=path.resolve(arg('--resourcepack'));
if(!fs.existsSync(path.join(dpRoot,'pack.mcmeta'))||!fs.existsSync(path.join(rpRoot,'pack.mcmeta')))throw new Error('Both targets must contain pack.mcmeta.');
const dp=path.join(dpRoot,'data/rlk/function/cm'),rp=path.join(rpRoot,'assets/rlk');
const put=(p,s)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,s.endsWith('\n')?s:s+'\n','utf8');};
const fn=(n,s)=>put(path.join(dp,n+'.mcfunction'),s);
const json=(p,o)=>put(p,JSON.stringify(o,null,2));
const parts=['head','body','right_arm','left_arm','right_leg','left_leg','shield'];
function faces(u,v,w,h,d){
 const f=(x1,y1,x2,y2)=>({uv:[x1/4,y1/4,x2/4,y2/4],texture:'#skin',tintindex:0});
 return {east:f(u,v+d,u+d,v+d+h),north:f(u+d,v+d,u+d+w,v+d+h),west:f(u+d+w,v+d,u+2*d+w,v+d+h),south:f(u+2*d+w,v+d,u+2*d+2*w,v+d+h),up:f(u+d,v,u+d+w,v+d),down:f(u+d+w,v+d,u+d+2*w,v)};
}
const box=(a,b,uv,grow=0)=>({from:a.map(v=>v-grow),to:b.map(v=>v+grow),faces:faces(...uv)});
function solid(from,to,tex,uv=[0,0,16,16]){return {from,to,faces:Object.fromEntries(['north','south','east','west','up','down'].map(f=>[f,{texture:'#'+tex,uv,tintindex:0}]))};}
const shapes={
 head:{a:[4,8,4],b:[12,16,12],uv:[0,0,8,8,8],over:[32,0,8,8,8],grow:.5},
 body:{a:[4,-4,6],b:[12,8,10],uv:[16,16,8,12,4],over:[16,32,8,12,4],grow:.25},
 right_arm:{a:[6,-2,6],b:[10,10,10],uv:[40,16,4,12,4],over:[40,32,4,12,4],grow:.25},
 left_arm:{a:[6,-2,6],b:[10,10,10],uv:[32,48,4,12,4],over:[48,48,4,12,4],grow:.25},
 right_leg:{a:[6,-4,6],b:[10,8,10],uv:[0,16,4,12,4],over:[0,32,4,12,4],grow:.25},
 left_leg:{a:[6,-4,6],b:[10,8,10],uv:[16,48,4,12,4],over:[0,48,4,12,4],grow:.25}
};
for(const [name,s] of Object.entries(shapes)){
 const model={ambientocclusion:false,textures:{skin:'rlk:skin/mob_sh',metal:'rlk:cm/sh/iron_block',dark:'rlk:cm/sh/polished_deepslate',particle:'rlk:skin/mob_sh'},elements:[box(s.a,s.b,s.uv),box(s.a,s.b,s.over,s.grow)]};
 if(name==='head')model.elements.push(solid([3,14,3],[13,17,13],'metal',[4,4,12,12]),solid([3,8,12],[13,14,13],'metal',[4,4,12,12]),solid([3,8,3],[4,14,12],'metal',[4,4,12,12]),solid([12,8,3],[13,14,12],'metal',[4,4,12,12]),solid([4,13,3],[12,14,4],'dark'));
 if(name==='body')model.elements.push(solid([3.6,-.5,5.2],[12.4,8.4,6],'metal',[3,3,13,13]),solid([3.6,-.5,10],[12.4,8.4,10.8],'metal',[3,3,13,13]),solid([3.6,-1,5.1],[12.4,.2,10.9],'dark'));
 if(name.endsWith('_arm'))model.elements.push(solid([5.5,6,5.5],[10.5,10.5,10.5],'metal',[4,4,12,12]));
 json(path.join(rp,'models/item/cm/sh',name+'.json'),model);
}
// An original broad, iron-edged pavise. Its bottom corners actually reach the
// ground during the drag poses; the wrist stays attached to the same arm joint.
json(path.join(rp,'models/item/cm/sh/shield.json'),{ambientocclusion:false,textures:{wood:'rlk:cm/sh/dark_oak_planks',metal:'rlk:cm/sh/iron_block',dark:'rlk:cm/sh/polished_deepslate',particle:'rlk:cm/sh/iron_block'},elements:[
 solid([1,-6,6],[15,19,7.5],'wood'),solid([0,-6,5.7],[1.5,19,7.8],'metal'),solid([14.5,-6,5.7],[16,19,7.8],'metal'),
 solid([0,18,5.7],[16,20,7.8],'metal'),solid([0,-7,5.5],[16,-5.3,8],'dark'),
 solid([6.5,-5,5.3],[9.5,18,6],'metal'),solid([1,6,5.2],[15,8,6],'metal'),solid([5.5,4.5,4.3],[10.5,9.5,5.3],'dark'),
 solid([5.5,5.3,7.5],[6.7,10.7,10],'dark'),solid([9.3,5.3,7.5],[10.5,10.7,10],'dark'),solid([5.5,7.4,9.3],[10.5,8.6,10.5],'wood')
]});
for(const p of parts)json(path.join(rp,'items/cm/sh',p+'.json'),{model:{type:'minecraft:model',model:'rlk:item/cm/sh/'+p,tints:[{type:'minecraft:custom_model_data',index:0,default:16777215}]}});
const rad=x=>x*Math.PI/180;
function mul(a,b){const[x,y,z,w]=a,[X,Y,Z,W]=b;return[w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W,w*W-x*X-y*Y-z*Z];}
function q(e=[0,0,0]){const[x,y,z]=e.map(v=>rad(v)/2);return mul(mul([0,0,Math.sin(z),Math.cos(z)],[0,Math.sin(y),0,Math.cos(y)]),[Math.sin(x),0,0,Math.cos(x)]);}
const rot=(a,v)=>mul(mul(a,[...v,0]),[-a[0],-a[1],-a[2],a[3]]).slice(0,3);
const add=(a,b)=>a.map((v,i)=>v+b[i]);
const guard={torso:[7,0,0],head:[-5,0,0],right_arm:[44,-8,-15],left_arm:[12,0,15],right_leg:[-7,0,-4],left_leg:[9,0,4],shield:[-5,-7,-6]};
function rig(over={}){
 const p={...guard,...over},hip=add([0,.75,0],p.shift||[0,0,0]),t=q(p.torso),root=q(p.root||[0,0,0]),size=1.25*(p.size??1),r={};
 const shoulder=add(hip,rot(t,[0,.75,0]));
 r.body={t:shoulder,q:t};r.head={t:shoulder,q:mul(t,q(p.head))};
 for(const [name,sign] of [['right_arm',-1],['left_arm',1]])r[name]={t:add(hip,rot(t,[sign*.375,.625,0])),q:mul(t,q(p[name]))};
 for(const [name,sign] of [['right_leg',-1],['left_leg',1]])r[name]={t:add(hip,[sign*.125,0,0]),q:q(p[name])};
 r.shield={t:add(r.right_arm.t,rot(r.right_arm.q,[0,-.535,-.015])),q:q(p.shield)};
 for(const a of Object.values(r)){a.t=add(p.rootShift||[0,0,0],rot(root,a.t).map(v=>v*size));a.q=mul(root,a.q);a.s=[size,size,size];}
 // Lower the whole crouched silhouette to the shield's bottom contact point.
 // All body-to-grip offsets remain rigid. No detached sliding shield is used.
 if(p.drag){let low=Infinity;for(const x of [-.5,.5])for(const z of [-.15625,0])low=Math.min(low,r.shield.t[1]+rot(r.shield.q,[x*size,-.9375*size,z*size])[1]);for(const a of Object.values(r))a.t[1]+=.035-low;}
 for(const a of Object.values(r)){a.t=[a.t[0],a.t[1],-a.t[2]];a.q=[-a.q[0],-a.q[1],a.q[2],a.q[3]];}
 return r;
}
const fl=v=>String(Math.abs(v)<.0000005?0:Number(v.toFixed(6)))+'f';
const arr=a=>'['+a.map(fl).join(',')+']';
const poses=[];
function pose(id,name,duration,over){const r=rig(over);poses.push({id,name,duration,rig:r});fn('sh/rig/pose/'+id,'# Original shield soldier: '+name+'\n'+parts.map(p=>`data merge entity @e[tag=rlk_sh_this,tag=rlk_sh_${p},limit=1] {start_interpolation:0,interpolation_duration:${duration},transformation:{translation:${arr(r[p].t)},left_rotation:${arr(r[p].q)},scale:${arr(r[p].s)},right_rotation:[0f,0f,0f,1f]}}`).join('\n'));}
for(let i=0;i<4;i++){const a=i*Math.PI/2;pose(i,'heavy_guard_breath_'+i,12,{shift:[0,Math.sin(a)*.012,0],torso:[7+Math.sin(a)*1.5,0,Math.cos(a)*.7],head:[-5-Math.sin(a),0,0],right_arm:[44+Math.sin(a)*1.5,-8,-15]});}
for(let i=0;i<8;i++){const a=i*Math.PI/4,s=Math.sin(a);pose(10+i,'weighty_march_'+i,3,{shift:[0,Math.abs(Math.cos(a))*.021,0],torso:[11,s*3,-s*2],head:[-7,-s*3,0],right_arm:[44-s*3,-8,-15],left_arm:[12-s*18,0,15],right_leg:[s*23,0,-5],left_leg:[-s*23,0,5]});}
pose(20,'bash_pull_back',4,{shift:[0,-.035,.025],torso:[9,20,-6],head:[-7,-20,2],right_arm:[35,33,-30],left_arm:[32,-4,25],shield:[-9,32,-14]});
pose(21,'bash_loaded',4,{shift:[0,-.065,.04],torso:[12,32,-8],head:[-9,-32,4],right_arm:[28,45,-36],left_arm:[43,-6,30],right_leg:[-15,0,-8],left_leg:[20,0,8],shield:[-13,48,-18]});
pose(22,'bash_begin_sweep',2,{shift:[0,-.055,0],torso:[12,19,-4],head:[-9,-19,1],right_arm:[57,15,-22],left_arm:[30,5,28],right_leg:[-13,0,-8],left_leg:[20,0,8],shield:[-5,20,-8]});
pose(23,'bash_contact',2,{shift:[0,-.035,-.07],torso:[15,-22,6],head:[-12,22,-3],right_arm:[92,-18,8],left_arm:[12,15,26],right_leg:[20,0,-7],left_leg:[-15,0,7],shield:[5,-28,9]});
pose(30,'lower_shield',6,{shift:[0,-.025,.01],torso:[-12,4,-4],head:[9,-4,1],right_arm:[56,3,-18],left_arm:[29,0,27],right_leg:[-10,0,-9],left_leg:[16,0,9],shield:[-13,8,-7]});
pose(31,'set_shield_edge',6,{drag:true,torso:[-20,3,-4],head:[17,-3,2],right_arm:[64,5,-20],left_arm:[41,0,28],right_leg:[-20,0,-10],left_leg:[29,0,10],shield:[-14,8,-8]});
pose(32,'drive_forward',3,{drag:true,torso:[-24,0,-5],head:[21,0,3],right_arm:[68,4,-20],left_arm:[50,-8,27],right_leg:[-24,0,-9],left_leg:[33,0,9],shield:[-16,6,-8]});
for(let i=0;i<4;i++){const s=Math.sin(i*Math.PI/2);pose(40+i,'shield_scrape_rush_'+i,2,{drag:true,torso:[-24,0,-4+s],head:[21,0,2],right_arm:[68,4,-20],left_arm:[38-s*18,-5,28],right_leg:[s*39,0,-7],left_leg:[-s*39,0,7],shield:[-16,6,-8]});}
pose(50,'lift_after_drag',3,{shift:[0,-.05,0],torso:[18,8,-5],head:[-15,-8,2],right_arm:[49,24,-24],left_arm:[43,-7,28],right_leg:[-14,0,-9],left_leg:[23,0,9],shield:[-9,29,-12]});
pose(51,'rush_bash_load',3,{shift:[0,-.04,.02],torso:[14,27,-7],head:[-11,-27,3],right_arm:[62,34,-26],left_arm:[39,-4,30],right_leg:[-12,0,-8],left_leg:[23,0,8],shield:[-6,35,-14]});
pose(52,'rush_bash_contact',2,{shift:[0,-.025,-.09],torso:[19,-24,9],head:[-16,24,-5],right_arm:[100,-22,13],left_arm:[8,17,31],right_leg:[24,0,-7],left_leg:[-17,0,7],shield:[8,-34,14]});
pose(60,'bash_follow_through',3,{shift:[0,-.055,-.05],torso:[17,-33,8],head:[-14,33,-4],right_arm:[76,-37,29],left_arm:[14,9,25],right_leg:[21,0,-6],left_leg:[-13,0,6],shield:[6,-39,18]});
pose(61,'bring_shield_back',3,{shift:[0,-.025,-.02],torso:[12,-14,4],head:[-9,14,-2],right_arm:[56,-20,2],left_arm:[15,5,21],shield:[0,-16,3]});
pose(62,'return_to_guard',2,guard);
pose(70,'hit_absorb',2,{shift:[0,-.05,.035],torso:[-6,8,-8],head:[9,-8,5],right_arm:[34,8,-29],left_arm:[43,-15,29],right_leg:[-16,0,-8],left_leg:[21,0,8],shield:[-12,17,-17]});
pose(71,'hit_recover',3,{shift:[0,-.025,.015],torso:[0,4,-4],head:[3,-4,2],right_arm:[38,0,-22],left_arm:[27,-6,21],shield:[-8,5,-11]});
pose(80,'death_kneel',3,{shift:[0,-.21,0],torso:[28,11,-15],head:[23,-9,-7],right_arm:[19,10,-23],left_arm:[40,14,27],right_leg:[-24,0,-13],left_leg:[36,0,13],shield:[-22,25,-18]});
pose(81,'death_topple',4,{root:[8,0,-47],rootShift:[0,.22,0],shift:[0,-.055,0],torso:[9,8,-6],head:[20,2,6],right_arm:[8,4,-11],left_arm:[25,8,28],right_leg:[-10,0,-5],left_leg:[20,0,5],shield:[-4,24,1]});
pose(82,'death_ground',3,{root:[0,0,-88],rootShift:[0,.37,0],torso:[6,0,0],head:[15,8,4],right_arm:[4,0,-10],left_arm:[28,8,25],right_leg:[-7,0,0],left_leg:[17,0,3],shield:[-1,20,5]});
pose(83,'death_dissolve',4,{root:[0,0,-88],rootShift:[0,.12,0],torso:[6,0,0],head:[15,8,4],right_arm:[4,0,-10],left_arm:[28,8,25],right_leg:[-7,0,0],left_leg:[17,0,3],shield:[-1,20,5],size:.04});
fn('sh/rig/apply',poses.filter(p=>p.id<80).map(p=>`execute if score #shPose tmp matches ${p.id} run function rlk:cm/sh/rig/pose/${p.id}`).join('\n'));
json(path.join(base,'shield_poses.json'),{authoring:'Original shield soldier keyframes; no reference motion or geometry copied.',space:'Runtime item_display: +Z forward, right hand -X; renderer model Y180 follows this transform.',parts,poses});

fn('sh/rig/select',`# cmId is the sole ownership key, including the surviving corpse anchor.
tag @e[tag=rlk_sh_this] remove rlk_sh_this
scoreboard players operation #shId tmp = @s cmId
execute as @e[tag=rlk_sh_rig] if score @s cmId = #shId tmp run tag @s add rlk_sh_this`);
fn('sh/rig/rebuild',`# Reload migration and partial-rig repair; shield durability is preserved.
function rlk:cm/sh/rig/select
kill @e[tag=rlk_sh_this]
execute as @e[tag=rlk_cmv] if score @s cmId = #shId tmp run kill @s
scoreboard players set @s cmAF 0
scoreboard players set @s cmAH 0
scoreboard players set @s cmAR 0
scoreboard players set @s cmAP -1
execute store result score @s cmAX run data get entity @s Pos[0] 1000
execute store result score @s cmAZ run data get entity @s Pos[2] 1000
function rlk:cm/sh/rig/create`);
let spawn='# Six body joints, one shield and a feet-origin owner anchor.\n';
spawn+='summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_sh_rig","rlk_sh_anchor","rlk_cmlink","rlk_cmsync","rlk_sh_new"]}\n';
for(const p of parts)spawn+=`summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_pet","rlk_sh_rig","rlk_sh_part","rlk_sh_${p}","rlk_cmlink","rlk_cmsync","rlk_sh_new"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:1.5f,width:4.5f,height:4.5f,shadow_radius:0f,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:cm/sh/${p}","minecraft:custom_model_data":{colors:[16777215]}}}}\n`;
spawn+=`scoreboard players operation @e[tag=rlk_sh_new] cmId = #shId tmp
tag @e[tag=rlk_sh_new] add rlk_sh_this
tag @e[tag=rlk_sh_new] remove rlk_sh_new
scoreboard players set @e[tag=rlk_sh_this,tag=rlk_sh_anchor] cmAD 0
function rlk:cm/sh/rig/pose/0
execute if score @s cmSh matches ..0 run function rlk:cm/sh/rig/hide_shield
tag @e[tag=rlk_sh_this] remove rlk_sh_this`;
fn('sh/rig/create',spawn);
fn('sh/rig/hide_shield',`# @s remains the owning brain. Keep the empty joint for transforms/repair counts.
data remove entity @e[tag=rlk_sh_this,tag=rlk_sh_shield,limit=1] item
tag @e[tag=rlk_sh_this,tag=rlk_sh_shield] add rlk_sh_broken`);
fn('sh/rig/break',`# Remove immediately on the confirmed durability break, including mid-animation.
function rlk:cm/sh/rig/select
function rlk:cm/sh/rig/hide_shield
scoreboard players set @s cmAR 0
scoreboard players set @s cmAH 6
tag @e[tag=rlk_sh_this] remove rlk_sh_this`);
fn('sh/rig/hurt',`scoreboard players set @s cmAH 6
function rlk:cm/sh/rig/select
execute as @e[tag=rlk_sh_this,tag=rlk_sh_part,tag=!rlk_sh_broken] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16737903]}
tag @e[tag=rlk_sh_this] remove rlk_sh_this`);
fn('sh/rig/tick',`# @s = the shield soldier brain, at @s. Keep actual turn rate and rush facing.
function rlk:cm/sh/rig/select
execute store result score #shCount tmp if entity @e[tag=rlk_sh_this]
execute unless score #shCount tmp matches 8 run function rlk:cm/sh/rig/rebuild
execute unless score #shCount tmp matches 8 run function rlk:cm/sh/rig/select
tag @e[tag=rlk_sh_this] add rlk_cmsync
execute as @e[tag=rlk_cmlink,distance=..10] if score @s cmId = #shId tmp run tag @s add rlk_cmsync
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 as @e[tag=rlk_sh_this] run tp @s ~ ~ ~ ~ 0
execute if score @s cmSh matches ..0 unless entity @e[tag=rlk_sh_this,tag=rlk_sh_broken] run function rlk:cm/sh/rig/hide_shield
execute store result score #shX tmp run data get entity @s Pos[0] 1000
execute store result score #shZ tmp run data get entity @s Pos[2] 1000
scoreboard players operation #shDX tmp = #shX tmp
scoreboard players operation #shDZ tmp = #shZ tmp
scoreboard players operation #shDX tmp -= @s cmAX
scoreboard players operation #shDZ tmp -= @s cmAZ
scoreboard players set #shNeg tmp -1
execute if score #shDX tmp matches ..-1 run scoreboard players operation #shDX tmp *= #shNeg tmp
execute if score #shDZ tmp matches ..-1 run scoreboard players operation #shDZ tmp *= #shNeg tmp
scoreboard players operation #shMove tmp = #shDX tmp
scoreboard players operation #shMove tmp += #shDZ tmp
scoreboard players operation @s cmAX = #shX tmp
scoreboard players operation @s cmAZ = #shZ tmp
execute if score @s cmAH matches 1 as @e[tag=rlk_sh_this,tag=rlk_sh_part,tag=!rlk_sh_broken] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if score @s frzT matches 1.. run return run function rlk:cm/sh/rig/frozen
scoreboard players add @s cmAF 1
execute if score @s cmAF matches 48.. run scoreboard players set @s cmAF 0
scoreboard players operation #shFrame tmp = @s cmAF
scoreboard players set #shDiv tmp 12
scoreboard players operation #shFrame tmp /= #shDiv tmp
scoreboard players operation #shPose tmp = #shFrame tmp
execute if score #shMove tmp matches 8.. run function rlk:cm/sh/rig/walk
execute if score @s cmAR matches 7.. run scoreboard players set #shPose tmp 60
execute if score @s cmAR matches 4..6 run scoreboard players set #shPose tmp 61
execute if score @s cmAR matches 1..3 run scoreboard players set #shPose tmp 62
execute if score @s cmS matches 1 run function rlk:cm/sh/rig/bash_wind
execute if score @s cmS matches 2 run function rlk:cm/sh/rig/rush_wind
execute if score @s cmS matches 3 run function rlk:cm/sh/rig/rush_pose
execute if score @s cmS matches 4 run function rlk:cm/sh/rig/rush_bash
execute unless entity @s[tag=rlk_cmch] if score @s cmAH matches 4.. run scoreboard players set #shPose tmp 70
execute unless entity @s[tag=rlk_cmch] if score @s cmAH matches 1..3 run scoreboard players set #shPose tmp 71
execute unless score @s cmAP = #shPose tmp run function rlk:cm/sh/rig/apply
scoreboard players operation @s cmAP = #shPose tmp
execute if score @s cmAR matches 1.. run scoreboard players remove @s cmAR 1
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_sh_this] remove rlk_sh_this`);
fn('sh/rig/walk',`scoreboard players operation #shFrame tmp = @s cmAF
scoreboard players set #shDiv tmp 24
scoreboard players operation #shFrame tmp %= #shDiv tmp
scoreboard players set #shDiv tmp 3
scoreboard players operation #shFrame tmp /= #shDiv tmp
scoreboard players operation #shPose tmp = #shFrame tmp
scoreboard players add #shPose tmp 10`);
fn('sh/rig/frozen',`execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_sh_this] remove rlk_sh_this`);
fn('sh/rig/bash_wind',`scoreboard players operation #shPhase tmp = @s cmT
scoreboard players set #shDiv tmp 3
scoreboard players operation #shPhase tmp *= #shDiv tmp
scoreboard players operation #shPhase tmp /= #cmW_sh tmp
scoreboard players set #shPose tmp 21
execute if score #shPhase tmp matches 2.. run scoreboard players set #shPose tmp 20
execute if score @s cmT matches 3..5 run scoreboard players set #shPose tmp 22
execute if score @s cmT matches 1..2 run scoreboard players set #shPose tmp 23`);
fn('sh/rig/rush_wind',`scoreboard players operation #shPhase tmp = @s cmT
scoreboard players set #shDiv tmp 3
scoreboard players operation #shPhase tmp *= #shDiv tmp
scoreboard players operation #shPhase tmp /= #cmW_shR tmp
scoreboard players set #shPose tmp 31
execute if score #shPhase tmp matches 2.. run scoreboard players set #shPose tmp 30
execute if score @s cmT matches 1..5 run scoreboard players set #shPose tmp 32`);
fn('sh/rig/rush_pose',`scoreboard players operation #shFrame tmp = @s cmAF
scoreboard players set #shDiv tmp 8
scoreboard players operation #shFrame tmp %= #shDiv tmp
scoreboard players set #shDiv tmp 2
scoreboard players operation #shFrame tmp /= #shDiv tmp
scoreboard players operation #shPose tmp = #shFrame tmp
scoreboard players add #shPose tmp 40
# Sparks are tied to the actual shield edge and disappear when the shield breaks.
execute if score @s cmSh matches 1.. rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^-0.7 ^0.045 ^0.9 run particle minecraft:crit ~ ~ ~ 0.04 0.005 0.08 0.025 2`);
fn('sh/rig/rush_bash',`scoreboard players set #shPose tmp 50
execute if score @s cmT matches 3..5 run scoreboard players set #shPose tmp 51
execute if score @s cmT matches 1..2 run scoreboard players set #shPose tmp 52`);
fn('sh/rig/die',`function rlk:cm/sh/rig/select
tag @e[tag=rlk_sh_this] add rlk_sh_dying
tag @e[tag=rlk_sh_this] add rlk_anim_dying
scoreboard players set @s cmAD 0
execute as @e[tag=rlk_sh_this,tag=rlk_sh_part,tag=!rlk_sh_broken] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
function rlk:cm/sh/rig/pose/80
tag @e[tag=rlk_sh_this] remove rlk_sh_this`);
fn('sh/rig/death_tick',`function rlk:cm/sh/rig/select
scoreboard players add @s cmAD 1
execute if score @s cmAD matches 4 run function rlk:cm/sh/rig/pose/81
execute if score @s cmAD matches 8 run function rlk:cm/sh/rig/pose/82
execute if score @s cmAD matches 11 run function rlk:cm/sh/rig/pose/83
execute if score @s cmAD matches 15.. run kill @e[tag=rlk_sh_this]
tag @e[tag=rlk_sh_this] remove rlk_sh_this`);

// Narrow repeatable edits, all confined to this mob's owned files.
function after(n,anchor,extra){const f=path.join(dp,n+'.mcfunction');let s=fs.readFileSync(f,'utf8').replace(/\r\n/g,'\n');if(s.includes(extra))return;if(!s.includes(anchor))throw new Error('Missing hook '+n);put(f,s.replace(anchor,anchor+'\n'+extra));}
let source=fs.readFileSync(path.join(dp,'spawn/sh.mcfunction'),'utf8').replace(/\r\n/g,'\n');
source=source.split('\n').filter(l=>!l.includes('minecraft:mannequin')&&!l.includes('rlk_cmvnew')).join('\n').replace('# 커스텀 몹 소환(실행 위치): 두뇌(투명 허스크) + 모습(마네킹)','# 방패병: 기존 1.25배 허스크 두뇌 + 독립적인 관절/방패 디스플레이');
put(path.join(dp,'spawn/sh.mcfunction'),source);
after('sh/bash','scoreboard players set @s cmS 0','scoreboard players set @s cmAR 10');
after('sh/sstart','scoreboard players set @s cmS 1','scoreboard players set @s cmAR 0');
after('sh/rstart','scoreboard players set @s cmS 2','scoreboard players set @s cmAR 0');
after('sh/break','scoreboard players set @s cmSh 0','function rlk:cm/sh/rig/break');
console.log(JSON.stringify({mob:'sh',models:parts.length,poses:poses.length,requiredAtlasSources:[{type:'minecraft:single',resource:'rlk:skin/mob_sh'},...['iron_block','polished_deepslate','dark_oak_planks'].map(b=>({type:'minecraft:single',resource:'minecraft:block/'+b,sprite:'rlk:cm/sh/'+b}))]},null,2));
