// Articulated Arlecchino / Skirk combat avatars, authored for this datapack.
// Existing skin PNGs are reused; all geometry and keyframes are local sources.
// node tools/build_player_rig.mjs --datapack <pack> --resourcepack <unpacked pack>
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {buildLocomotion} from './build_player_locomotion.mjs';
import {buildScytheGeometry} from './scythe_geometry.mjs';
import {buildSkirkWeaponGeometry} from './skirk_weapon_geometry.mjs';
import {paintWeaponTextures,spriteId} from './weapon_paint.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));
const arg=n=>{const i=process.argv.indexOf(n);return i<0?undefined:process.argv[i+1];};
const dpRoot=path.resolve(arg('--datapack')||path.join(here,'..'));
if(!arg('--resourcepack'))throw new Error('Provide --resourcepack.');
const rpRoot=path.resolve(arg('--resourcepack'));
const dst=path.join(dpRoot,'data/rlk/function/char/motion');
const assets=path.join(rpRoot,'assets/rlk');
const put=(p,s)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,s.endsWith('\n')?s:s+'\n','utf8');};
const fn=(n,s)=>put(path.join(dst,n+'.mcfunction'),s);
const json=(p,o)=>put(p,JSON.stringify(o,null,2));
const parts=['head','body','right_arm','right_forearm','left_arm','left_forearm','right_leg','right_shin','left_leg','left_shin','weapon'];
const characters={arle:{skin:'arlecchino',id:5,weapon:'spear'},skirk:{skin:'skirk',id:3,weapon:'sword'}};
const zeros=[0,0,0];
const fields=['shift','root','torso','head','right_arm','right_elbow','left_arm','left_elbow','right_leg','right_knee','left_leg','left_knee','weapon','weapon_shift'];
const neutral=()=>Object.fromEntries([...fields.map(k=>[k,[0,0,0]]),['weapon_scale',[1,1,1]]]);
const rad=d=>d*Math.PI/180;
function mul(a,b){const[x,y,z,w]=a,[X,Y,Z,W]=b;return[w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W,w*W-x*X-y*Y-z*Z];}
function quat(e=zeros){const[x,y,z]=e.map(a=>rad(a)/2);return mul(mul([0,0,Math.sin(z),Math.cos(z)],[0,Math.sin(y),0,Math.cos(y)]),[Math.sin(x),0,0,Math.cos(x)]);}
const rot=(q,v)=>mul(mul(q,[...v,0]),[-q[0],-q[1],-q[2],q[3]]).slice(0,3);
const add=(a,b)=>a.map((x,i)=>x+b[i]);
const lerp=(a,b,t)=>a.map((x,i)=>x+(b[i]-x)*t);
const f=x=>(Math.abs(x)<0.0000005?0:x).toFixed(6)+'f';
const arr=a=>'['+a.map(f).join(',')+']';
function transform(pose){
 const p={...neutral(),...pose},root=quat(p.root),body=quat(p.torso),hip=add([0,.75,0],p.shift),out={};
 const top=add(hip,rot(body,[0,.75,0]));
 out.body={t:top,q:body};out.head={t:top,q:mul(body,quat(p.head))};
 for(const [side,sign]of[['right',-1],['left',1]]){
  const shoulder=add(hip,rot(body,[sign*.34375,.625,0]));
  const arm=mul(body,quat(p[side+'_arm']));
  const elbow=add(shoulder,rot(arm,[0,-.25,0]));
  const fore=mul(arm,quat(p[side+'_elbow']));
  out[side+'_arm']={t:shoulder,q:arm};out[side+'_forearm']={t:elbow,q:fore};
  const leg=quat(p[side+'_leg']),pelvis=add(hip,[sign*.125,0,0]);
  out[side+'_leg']={t:pelvis,q:leg};
  out[side+'_shin']={t:add(pelvis,rot(leg,[0,-.375,0])),q:mul(leg,quat(p[side+'_knee']))};
  if(side==='right')out.weapon={t:add(add(elbow,rot(fore,[0,-.34375,0])),rot(fore,p.weapon_shift)),q:mul(fore,quat(p.weapon)),s:p.weapon_scale};
 }
 for(const [name,value] of Object.entries(out)){
  value.t=add(hip,rot(root,value.t.map((x,i)=>x-hip[i])));value.q=mul(root,value.q);
  // item_display model Y180 is applied after the NBT matrix. Preserve hand side.
  value.t=[value.t[0],value.t[1],-value.t[2]];
  value.q=[-value.q[0],-value.q[1],value.q[2],value.q[3]];
  if(name==='weapon'&&pose.scythe_loco){
   // Locomotion only: retain the authored shaft heading and hand position.
   // item_display's model Y180 maps the model's -X hook onto matrix +X.
   // Roll that hook to 30 degrees from straight down toward character right
   // (-X), measured in the character's frontal X/Y plane. Combat calibration
   // never passes this flag, so its edge-leading strike poses remain intact.
   const shaft=rot(value.q,[0,1,0]),oldHook=rot(value.q,[1,0,0]);
   const hook=[-.5,-Math.sqrt(3)/2,0];
   hook[2]=-(hook[0]*shaft[0]+hook[1]*shaft[1])/shaft[2];
   const length=Math.hypot(...hook),target=hook.map(x=>x/length);
   const cross=[oldHook[1]*target[2]-oldHook[2]*target[1],oldHook[2]*target[0]-oldHook[0]*target[2],oldHook[0]*target[1]-oldHook[1]*target[0]];
   const angle=Math.atan2(cross.reduce((sum,x,i)=>sum+x*shaft[i],0),oldHook.reduce((sum,x,i)=>sum+x*target[i],0));
   const sine=Math.sin(angle/2);
   value.q=mul([...shaft.map(x=>x*sine),Math.cos(angle/2)],value.q);
  }
 }
 return out;
}
const nbt=v=>`{translation:${arr(v.t)},left_rotation:${arr(v.q)},scale:${arr(v.s||[1,1,1])},right_rotation:[0f,0f,0f,1f]}`;
function skinFaces(u,v,w,h,d,start=0,end=h){
 const face=(a,b,c,e)=>({uv:[a/4,b/4,c/4,e/4],texture:'#skin'});
 return{east:face(u,v+d+start,u+d,v+d+end),north:face(u+d,v+d+start,u+d+w,v+d+end),west:face(u+d+w,v+d+start,u+2*d+w,v+d+end),south:face(u+2*d+w,v+d+start,u+2*d+2*w,v+d+end),up:face(u+d,v,u+d+w,v+d),down:face(u+d+w,v+d,u+d+2*w,v)};
}
const skinBox=(from,to,uv,start,end,inflate=0)=>({from:from.map(x=>x-inflate),to:to.map(x=>x+inflate),faces:skinFaces(...uv,start,end)});
function bodyModels(char,skin){
 const specs={
  head:{from:[4,8,4],to:[12,16,12],uv:[0,0,8,8,8],over:[32,0,8,8,8],start:0,end:8,inflate:.5},
  body:{from:[4,-4,6],to:[12,8,10],uv:[16,16,8,12,4],over:[16,32,8,12,4],start:0,end:12,inflate:.25},
  right_arm:{from:[6.5,4,6],to:[9.5,10,10],uv:[40,16,3,12,4],over:[40,32,3,12,4],start:0,end:6,inflate:.25},
  right_forearm:{from:[6.5,2,6],to:[9.5,8,10],uv:[40,16,3,12,4],over:[40,32,3,12,4],start:6,end:12,inflate:.25},
  left_arm:{from:[6.5,4,6],to:[9.5,10,10],uv:[32,48,3,12,4],over:[48,48,3,12,4],start:0,end:6,inflate:.25},
  left_forearm:{from:[6.5,2,6],to:[9.5,8,10],uv:[32,48,3,12,4],over:[48,48,3,12,4],start:6,end:12,inflate:.25},
  right_leg:{from:[6,2,6],to:[10,8,10],uv:[0,16,4,12,4],over:[0,32,4,12,4],start:0,end:6,inflate:.25},
  right_shin:{from:[6,2,6],to:[10,8,10],uv:[0,16,4,12,4],over:[0,32,4,12,4],start:6,end:12,inflate:.25},
  left_leg:{from:[6,2,6],to:[10,8,10],uv:[16,48,4,12,4],over:[0,48,4,12,4],start:0,end:6,inflate:.25},
  left_shin:{from:[6,2,6],to:[10,8,10],uv:[16,48,4,12,4],over:[0,48,4,12,4],start:6,end:12,inflate:.25}
 };
 for(const[name,s]of Object.entries(specs)){
  json(path.join(assets,'models/item/player_motion',char,name+'.json'),{ambientocclusion:false,textures:{skin:'rlk:skin/'+skin,particle:'rlk:skin/'+skin},elements:[skinBox(s.from,s.to,s.uv,s.start,s.end),skinBox(s.from,s.to,s.over,s.start,s.end,s.inflate)]});
  json(path.join(assets,'items/player_motion',char,name+'.json'),{model:{type:'minecraft:model',model:`rlk:item/player_motion/${char}/${name}`}});
 }
}
const blocks=['black_concrete','red_concrete','orange_concrete','white_concrete','light_blue_concrete','purple_concrete','cyan_concrete','gray_concrete','blue_concrete','light_gray_concrete'];
const solid=(from,to,tex,rotation)=>({from,to,faces:Object.fromEntries(['north','south','east','west','up','down'].map(k=>[k,{texture:'#'+tex,uv:[0,0,16,16]}])),...(rotation?{rotation}:{} )});
function weaponModels(){
 // Painted signature-weapon sprites (weapon_paint.mjs): Arlecchino's 붉은 달의 형상 scythe and
 // Skirk's 창백한 섬광 sword. Each model lists only the sprites it uses.
 paintWeaponTextures(rpRoot);
 const {spear,scythe}=buildScytheGeometry();
 const {sword,cryo_sword:cryo}=buildSkirkWeaponGeometry();
 for(const[name,elements]of Object.entries({spear,scythe,sword,cryo_sword:cryo})){
  for(const el of elements)for(const v of[...el.from,...el.to])if(v<-16||v>32)throw new Error(name+': element outside -16..32');
  const used=[...new Set(elements.flatMap(el=>Object.values(el.faces).map(f=>f.texture.slice(1))))];
  const textures=Object.fromEntries(used.map(n=>[n,spriteId(n)]));textures.particle=textures[used[0]];
  json(path.join(assets,'models/item/player_motion/weapons',name+'.json'),{ambientocclusion:false,textures,elements});
  json(path.join(assets,'items/player_motion/weapons',name+'.json'),{model:{type:'minecraft:model',model:'rlk:item/player_motion/weapons/'+name}});
 }
}
function poseLines(p,duration='$(step)',hidden=false){
 return Object.entries(transform(p)).map(([name,v])=>`${duration.includes('$')?'$':''}data merge entity @e[tag=rlk_pm,tag=rlk_pm_${name},limit=1] {interpolation_duration:${duration},start_interpolation:0,transformation:${nbt(hidden?{...v,s:[0,0,0]}:v)}}`).join('\n');
}
function weaponLines(weapon){
 const light=['scythe','cryo_sword'].includes(weapon)?'data merge entity @e[tag=rlk_pm_weapon,limit=1] {brightness:{block:15,sky:15}}':'data remove entity @e[tag=rlk_pm_weapon,limit=1] brightness';
 return`data modify entity @e[tag=rlk_pm_weapon,limit=1] item set value {id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:player_motion/weapons/${weapon}"}}\n${light}`;
}
function spawnLines(char,pose,weapon,hidden=false){
 const values=transform(pose);
 if(hidden)for(const value of Object.values(values))value.s=[0,0,0];
 return parts.map(name=>{
 const item=name==='weapon'?`rlk:player_motion/weapons/${weapon}`:`rlk:player_motion/${char}/${name}`;
 return`summon minecraft:item_display ~ ~ ~ {Tags:["rlk_view","rlk_pet","rlk_pm","rlk_pm_${name}"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:1.5f,width:8f,height:6f,shadow_radius:0f,${name==='weapon'&&['scythe','cryo_sword'].includes(weapon)?'brightness:{block:15,sky:15},':''}transformation:${nbt(values[name])},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${item}"}}}`;
 }).join('\n')+'\nexecute rotated as @s rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0\n';
}
function compileClip(char,name,clip){
 if(!Number.isInteger(clip.length)||clip.length<1)throw new Error(`Invalid clip length ${char}/${name}`);
 let prev=neutral(),weapon=clip.weapon||characters[char].weapon,hidden=false;
 const keys=clip.frames.map(frame=>{prev={...prev,...frame.pose};weapon=frame.weapon||weapon;hidden=frame.hidden??hidden;return{tick:frame.tick,pose:structuredClone(prev),weapon,hidden};}).sort((a,b)=>a.tick-b.tick);
 if(keys[0]?.tick!==0)throw new Error(`First frame must be tick 0: ${char}/${name}`);
 const sample=t=>{
  let a=keys[0],b=a;for(let i=0;i<keys.length;i++){if(keys[i].tick<=t)a=keys[i];if(keys[i].tick>t){b=keys[i];break;}b=a;}
  const fraction=b.tick===a.tick?0:(t-a.tick)/(b.tick-a.tick),pose={};
  for(const field of Object.keys(neutral()))pose[field]=lerp(a.pose[field],b.pose[field],fraction);
  return{pose,weapon:a.weapon,hidden:a.hidden};
 };
 const base=`clips/${char}/${name}`,dispatch=[];
 let lastWeapon;
 for(let t=0;t<=clip.length;t++){
  const current=sample(t),lines=[`# ${char} / ${name}: authored animation tick ${t}`,poseLines(current.pose,'$(step)',current.hidden)];
  if(current.weapon!==lastWeapon)lines.push(weaponLines(current.weapon));
  lastWeapon=current.weapon;fn(`${base}/pose/${t}`,lines.join('\n'));
  dispatch.push(`execute if score @s pmTick matches ${t} run function rlk:char/motion/${base}/pose/${t} with storage rlk:player_motion active`);
 }
 fn(`${base}/pose`,dispatch.join('\n'));
 fn(`${base}/spawn`,spawnLines(char,keys[0].pose,keys[0].weapon,keys[0].hidden));
 const normal=/^(physical|infused)_/.test(name);
 fn(`${base}/start`,[
  '# @s player. Existing avatar remains the gameplay body.',
  'function rlk:char/motion/release',
  'scoreboard players set @s pmBlend 0',
  'scoreboard players set @s pmWeapon -1',
  'scoreboard players set @s pmActive 1','scoreboard players set @s pmTick 0',`scoreboard players set @s pmLen ${clip.length}`,`scoreboard players set @s pmChar ${characters[char].id}`,
  'scoreboard players set @s pmSpeed 100',...(normal?['execute if score @s atkSpeed matches 1.. run scoreboard players operation @s pmSpeed = @s atkSpeed']:[]),
  ...(normal&&clip.playback_rate&&clip.playback_rate!==100?[
   `scoreboard players set #pmRate tmp ${clip.playback_rate}`,
   'scoreboard players operation @s pmSpeed *= #pmRate tmp',
   'scoreboard players operation @s pmSpeed /= #100 tmp'
  ]:[]),
  'execute if score @s pmSpeed matches ..24 run scoreboard players set @s pmSpeed 25','execute if score @s pmSpeed matches 501.. run scoreboard players set @s pmSpeed 500',
  'scoreboard players set @s pmAcc 0','scoreboard players set @s pmStep 99','scoreboard players operation @s pmStep += @s pmSpeed','scoreboard players operation @s pmStep /= @s pmSpeed',
  `data modify storage rlk:player_motion active set value {char:"${char}",clip:"${name}",step:1,loop:${clip.loop?'1b':'0b'},lockedYaw:${name.startsWith('burst')?'1b':'0b'}}`,
  'execute store result storage rlk:player_motion active.step int 1 run scoreboard players get @s pmStep',
  ...(name.startsWith('burst')?[
   'execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_pet","rlk_pm_basis"]}',
   'execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 run tp @e[tag=rlk_pm_basis,limit=1] ~ ~ ~ ~ 0'
  ]:[]),
  'execute unless score @s pmRigChar = #charN tmp run kill @e[tag=rlk_pm]',
  `execute if entity @e[tag=rlk_av,limit=1] unless entity @e[tag=rlk_pm] at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/${base}/spawn`,
  'execute if entity @e[tag=rlk_pm] run scoreboard players set @s pmVisible 1',
  'scoreboard players operation @s pmRigChar = #charN tmp',
  '# Reuse the displayed last pose when chaining an attack; interpolate into frame zero.',
  'data modify storage rlk:player_motion active.step set value 2',
  `execute if entity @e[tag=rlk_pm] run function rlk:char/motion/${base}/pose/0 with storage rlk:player_motion active`,
  'execute store result storage rlk:player_motion active.step int 1 run scoreboard players get @s pmStep',
  'execute at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0',
  'execute if entity @e[tag=rlk_av,limit=1] run function rlk:char/motion/hide_avatar',
  `execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/${char}_fx/${name}`,
  'execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/event',
  'return 1'
 ].join('\n'));
 const {frames,fx,...metadata}=clip;
 return{...metadata,char,name,length:clip.length,normal,weapon:clip.weapon||characters[char].weapon};
}
function runtime(){
 fn('init',['# Called by load. Objective additions are idempotent in Minecraft.',...['pmActive','pmTick','pmLen','pmChar','pmSpeed','pmAcc','pmStep'].map(o=>`scoreboard objectives add ${o} dummy`),'execute as @a[tag=player] run function rlk:char/motion/stop','kill @e[tag=rlk_pm]','kill @e[tag=rlk_pm_basis]'].join('\n'));
 fn('start','$function rlk:char/motion/clips/$(char)/$(clip)/start');
 fn('hide_avatar','effect give @e[tag=rlk_av,limit=1] minecraft:invisibility infinite 0 true\nitem replace entity @e[tag=rlk_av,limit=1] weapon.mainhand with minecraft:air\nitem replace entity @e[tag=rlk_av,limit=1] weapon.offhand with minecraft:air');
 fn('stop',[
  '# @s player. Do not alter avatar health, collision, AI, camera or position.',
  'execute if score @s pmActive matches 1 run function rlk:char/motion/control/cancel',
  'execute if data storage rlk:player_motion active.clip run function rlk:char/motion/audio/stop with storage rlk:player_motion active',
  'function rlk:char/motion/control/unlock',
  'scoreboard players set @s pmActive 0','scoreboard players set @s pmTick 0','scoreboard players set @s pmAcc 0','scoreboard players set @s pmAtkPending 0','kill @e[tag=rlk_pm]','kill @e[tag=rlk_pm_basis]',
  'execute if entity @e[tag=rlk_av,limit=1] run effect clear @e[tag=rlk_av,limit=1] minecraft:invisibility',
  'execute if entity @e[tag=rlk_av,limit=1] run item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand from entity @s hotbar.0',
  'execute if entity @e[tag=rlk_av,limit=1] run function rlk:view/av_unwrap',
  'execute if score #charN tmp matches 7..8 run item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand with minecraft:air'
 ].join('\n'));
 fn('tick',[
  '# @s player, once per game tick after the avatar has moved.',
  'execute unless score @s pmActive matches 1 run return 0',
  'execute unless score @s pmChar = #charN tmp run return run function rlk:char/motion/stop',
  'execute if score @s dead matches 1 run return run function rlk:char/motion/stop',
  'execute if score @s vMap matches 1 run return run function rlk:char/motion/stop',
  'execute if score @s pkMode matches 1.. run return run function rlk:char/motion/stop',
  'execute unless entity @e[tag=rlk_body,limit=1] run return run function rlk:char/motion/stop',
  'execute if data storage rlk:player_motion active{lockedYaw:1b} unless entity @e[tag=rlk_pm_basis,limit=1] run return run function rlk:char/motion/stop',
  'execute unless entity @e[tag=rlk_av,limit=1] run kill @e[tag=rlk_pm]',
  'execute if entity @e[tag=rlk_av,limit=1] unless entity @e[tag=rlk_pm] at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/respawn with storage rlk:player_motion active',
  'execute if entity @e[tag=rlk_av,limit=1] run function rlk:char/motion/hide_avatar',
  'execute unless data storage rlk:player_motion active{lockedYaw:1b} at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0',
  'execute if data storage rlk:player_motion active{lockedYaw:1b} at @e[tag=rlk_av,limit=1] rotated as @e[tag=rlk_pm_basis,limit=1] rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0',
  'scoreboard players operation @s pmAcc += @s pmSpeed',
  'execute if score @s pmAcc matches 100.. unless data storage rlk:player_motion active{lockedYaw:1b} at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/advance',
  'execute if score @s pmAcc matches 100.. if data storage rlk:player_motion active{lockedYaw:1b} at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_pm_basis,limit=1] rotated ~ 0 run function rlk:char/motion/advance'
 ].join('\n'));
 fn('respawn','$function rlk:char/motion/clips/$(char)/$(clip)/spawn');
 fn('advance',[
  'scoreboard players remove @s pmAcc 100','scoreboard players add @s pmTick 1',
  'execute if score @s pmTick > @s pmLen if data storage rlk:player_motion active{loop:1b} run scoreboard players set @s pmTick 0',
  'execute if score @s pmTick > @s pmLen run return run function rlk:char/motion/stop',
  'function rlk:char/motion/apply with storage rlk:player_motion active',
  'execute if score @s pmActive matches 1 if score @s pmAcc matches 100.. run function rlk:char/motion/advance'
 ].join('\n'));
 fn('apply','$execute if entity @e[tag=rlk_pm] run function rlk:char/motion/clips/$(char)/$(clip)/pose\n$function rlk:char/motion/$(char)_fx/$(clip)\nfunction rlk:char/motion/event');
}
for(const[char,info]of Object.entries(characters))bodyModels(char,info.skin);
weaponModels();runtime();
const manifest=[];
for(const char of Object.keys(characters)){
 const source=path.join(here,'player_motion',char+'.json');
 if(!fs.existsSync(source))continue;
 const data=JSON.parse(fs.readFileSync(source,'utf8'));
 for(const[name,clip]of Object.entries(data.clips))manifest.push(compileClip(char,name,clip));
}
const atlasPath=path.join(rpRoot,'assets/minecraft/atlases/items.json');
const atlas=fs.existsSync(atlasPath)?JSON.parse(fs.readFileSync(atlasPath,'utf8')):{sources:[]};
for(const block of blocks){const sprite='rlk:player_motion/'+block;atlas.sources=atlas.sources.filter(s=>s.sprite!==sprite);atlas.sources.push({type:'minecraft:single',resource:'minecraft:block/'+block,sprite});}
for(const info of Object.values(characters))if(!atlas.sources.some(s=>s.type==='minecraft:single'&&s.resource==='rlk:skin/'+info.skin&&!s.sprite))atlas.sources.push({type:'minecraft:single',resource:'rlk:skin/'+info.skin});
buildLocomotion({fn,poseLines,spawnLines,weaponLines,neutral,lerp,characters,here});
// Dash: player/dash_go calls this; a character with a "dash" clip plays it (gameplay moves the body).
fn('dash',['# @s = player, from player/dash_go: play the character dash clip when it has one.',...Object.entries(characters).filter(([c])=>{const src=path.join(here,'player_motion',c+'.json');return fs.existsSync(src)&&JSON.parse(fs.readFileSync(src,'utf8')).clips.dash;}).map(([c,info])=>`execute if score #charN tmp matches ${info.id} run function rlk:char/motion/start {char:"${c}",clip:"dash"}`)].join('\n'));
json(atlasPath,atlas);json(path.join(here,'player_motion/compiled_clips.json'),manifest);
console.log(`Built articulated combat avatars and ${manifest.length} clips.`);
