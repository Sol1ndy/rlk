// Articulated combat avatars (Arlecchino, Skirk, Navia, ...), authored for this datapack.
// Existing skin PNGs are reused; all geometry and keyframes are local sources.
// Adding a rig character is data-only: an entry in `characters` below, tools/player_motion/<key>.json
// (clips + "sheath" back mount; more clips may live in tools/player_motion/<key>/*.json fragments) and
// characters.<key> in tools/player_motion/locomotion.json. Normal clips (physical_/infused_) also generate
// M/combat/config/<key>/<clip> from hit_ticks/chain_tick.
// node tools/build_player_rig.mjs --datapack <pack> --resourcepack <unpacked pack>
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {buildLocomotion} from './build_player_locomotion.mjs';
import {buildScytheGeometry} from './scythe_geometry.mjs';
import {buildSkirkWeaponGeometry} from './skirk_weapon_geometry.mjs';
import {buildNaviaWeaponGeometry} from './navia_weapon_geometry.mjs';
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
// Rig characters, keyed by the name used in clip paths. Every per-character runtime branch
// (motion/tick gate, loco/context, loco/weapon, glow, scythe_loco, sheath/*) is generated from here.
//  id          #charN of the character
//  skin        rlk:skin/<skin> texture for the 10 body parts
//  weapon      default weapon model (clips without "weapon", locomotion spawns)
//  weaponScale multiplier on every weapon_scale: clip poses, spawns, locomotion, back and world attach
//  scytheLoco  locomotion-only post-roll of the in-hand hook (Arlecchino's scythe)
//  glow        weapon models drawn at full brightness (brightness 15)
//  locoWeapons ordered [{weapon, if?}]: outside clips, and in sheathed or put-away clips, the last entry whose
//              `if` (an execute condition) holds is the model shown; its index in the combined list is pmWantW
const characters={
 arle:{id:5,skin:'arlecchino',weapon:'spear',weaponScale:1,scytheLoco:true,glow:['scythe'],locoWeapons:[{weapon:'spear'},{weapon:'scythe',if:'score @s arM matches 1..'}]},
 skirk:{id:3,skin:'skirk',weapon:'sword',weaponScale:1,scytheLoco:false,glow:['cryo_sword'],locoWeapons:[{weapon:'sword'},{weapon:'cryo_sword',if:'score @s skM matches 1..'}]},
 navia:{id:6,skin:'navia',weapon:'navia_halberd',weaponScale:1.25,scytheLoco:false,glow:[],locoWeapons:[{weapon:'navia_halberd'}]}
};
// Clip and back-mount data, read once: tools/player_motion/<char>.json plus optional clip fragments
// tools/player_motion/<char>/*.json (each {"clips":{...}}), so several authors can own separate files.
// A clip name may appear only once across the main file and all fragments.
function loadMotion(dir,char){
 const source=path.join(dir,char+'.json');
 if(!fs.existsSync(source))throw new Error(`Missing ${source} for rig character ${char}.`);
 const data=JSON.parse(fs.readFileSync(source,'utf8'));
 const clips=data.clips=data.clips||{},origin=Object.fromEntries(Object.keys(clips).map(name=>[name,char+'.json']));
 const fragments=path.join(dir,char);
 if(fs.existsSync(fragments))for(const file of fs.readdirSync(fragments).filter(f=>f.endsWith('.json')).sort()){
  const part=JSON.parse(fs.readFileSync(path.join(fragments,file),'utf8'));
  if(!part.clips||typeof part.clips!=='object')throw new Error(`${char}/${file}: a clip fragment must be {"clips":{...}}.`);
  for(const[name,clip]of Object.entries(part.clips)){
   if(origin[name])throw new Error(`Duplicate clip "${name}" for ${char}: ${origin[name]} and ${char}/${file}.`);
   origin[name]=`${char}/${file}`;clips[name]=clip;
  }
 }
 return data;
}
const motionData={};
for(const[char,info]of Object.entries(characters)){
 const data=motionData[char]=loadMotion(path.join(here,'player_motion'),char);
 info.weaponScale??=1;info.scytheLoco??=false;info.glow??=[];info.locoWeapons??=[{weapon:info.weapon}];
 // sheath: {offset:[x,y,z] blocks from the neck point in the torso frame, euler:[x,y,z] degrees in the torso
 // frame, scale?, delay? ticks before putting the weapon away, grow? quick-stow re-form steps (sheath/fx_tick in
 // build_player_locomotion.mjs), weapons?:{<model>:{offset?,euler?,scale?}}}.
 // weapons overrides apply to models a drawn clip names while on the back. Sheathed locomotion, its spawn, the
 // quick stow and the sheathed or put-away clips show whichever locoWeapons variant loco/weapon picked at runtime,
 // always with the default model's mount, so every variant must keep that mount (checked here).
 info.sheath=data.sheath;
 if(!info.sheath?.offset||!info.sheath?.euler)throw new Error(`${char}.json needs "sheath":{"offset":[x,y,z],"euler":[x,y,z]} (weapon on the back).`);
 const variants=[...new Set([info.weapon,...info.locoWeapons.map(entry=>entry.weapon)])];
 for(const weapon of variants)if(JSON.stringify(sheathOf(char,weapon))!==JSON.stringify(sheathOf(char,info.weapon)))
  throw new Error(`${char}.json sheath.weapons: ${variants.join(', ')} are loco/weapon variants shown on the back with one shared mount; give ${weapon} no separate mount (edit the base sheath block instead).`);
 info.hasSheathe=!!data.clips?.sheathe;
}
const glowing=new Set(Object.values(characters).flatMap(info=>info.glow));
// Back mount of one weapon model: the character's sheath block with that model's overrides.
function sheathOf(char,weapon){const{weapons,delay,grow,note,...mount}=characters[char].sheath;return{scale:1,...mount,...(weapons?.[weapon]||{})};}
// Pose handed to transform(): weapon_scale times the character multiplier, the attach mode and its back mount.
function rigPose(char,pose,attach='hand',weapon=characters[char].weapon,extra={}){
 return{...pose,...extra,weapon_attach:attach,weapon_scale:(pose.weapon_scale||[1,1,1]).map(x=>x*characters[char].weaponScale),...(attach==='back'?{sheath:sheathOf(char,weapon)}:{})};
}
const attachIds={hand:0,back:1,world:2};
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
// pose.weapon_attach (D3): "hand" (default) = right forearm + weapon_shift + weapon euler; "back" = torso frame
// from the neck point with pose.sheath {offset,euler,scale}, weapon/weapon_shift ignored; "world" = detached in
// the clip frame (feet origin, rig yaw): translation weapon_shift, rotation weapon, no shift/root/torso.
function transform(pose){
 const p={...neutral(),...pose},root=quat(p.root),body=quat(p.torso),hip=add([0,.75,0],p.shift),out={};
 const attach=pose.weapon_attach||'hand';
 if(!(attach in attachIds))throw new Error(`Unknown weapon_attach "${attach}".`);
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
  if(side!=='right')continue;
  if(attach==='back'){
   const mount=pose.sheath;
   if(!mount)throw new Error('weapon_attach "back" needs the character sheath mount.');
   out.weapon={t:add(top,rot(body,mount.offset)),q:mul(body,quat(mount.euler)),s:p.weapon_scale.map(x=>x*(mount.scale??1))};
  }else if(attach==='world')out.weapon={t:[...p.weapon_shift],q:quat(p.weapon),s:p.weapon_scale};
  else out.weapon={t:add(add(elbow,rot(fore,[0,-.34375,0])),rot(fore,p.weapon_shift)),q:mul(fore,quat(p.weapon)),s:p.weapon_scale};
 }
 for(const [name,value] of Object.entries(out)){
  if(!(name==='weapon'&&attach==='world')){value.t=add(hip,rot(root,value.t.map((x,i)=>x-hip[i])));value.q=mul(root,value.q);}
  // item_display model Y180 is applied after the NBT matrix. Preserve hand side.
  value.t=[value.t[0],value.t[1],-value.t[2]];
  value.q=[-value.q[0],-value.q[1],value.q[2],value.q[3]];
  if(name==='weapon'&&pose.scythe_loco&&attach==='hand'){
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
const weaponSpan={}; // model px along +Y (butt..tip) per weapon model, for the sheath sparkle lines
function weaponModels(){
 // Painted signature-weapon sprites (weapon_paint.mjs): Arlecchino's 붉은 달의 형상 scythe,
 // Skirk's 창백한 섬광 sword, and Navia's halberd and parasol gun (closed / open, swapped per
 // frame). Each model lists only the sprites it uses.
 paintWeaponTextures(rpRoot);
 const {spear,scythe}=buildScytheGeometry();
 const {sword,cryo_sword:cryo}=buildSkirkWeaponGeometry();
 for(const[name,elements]of Object.entries({spear,scythe,sword,cryo_sword:cryo,...buildNaviaWeaponGeometry()})){
  for(const el of elements)for(const v of[...el.from,...el.to])if(v<-16||v>32)throw new Error(name+': element outside -16..32');
  weaponSpan[name]=[Math.min(...elements.flatMap(el=>[el.from[1],el.to[1]])),Math.max(...elements.flatMap(el=>[el.from[1],el.to[1]]))];
  const used=[...new Set(elements.flatMap(el=>Object.values(el.faces).map(f=>f.texture.slice(1))))];
  const textures=Object.fromEntries(used.map(n=>[n,spriteId(n)]));textures.particle=textures[used[0]];
  json(path.join(assets,'models/item/player_motion/weapons',name+'.json'),{ambientocclusion:false,textures,elements});
  json(path.join(assets,'items/player_motion/weapons',name+'.json'),{model:{type:'minecraft:model',model:'rlk:item/player_motion/weapons/'+name}});
 }
}
// snap: parts whose line uses interpolation_duration 0 (the weapon on an attach change).
function poseLines(p,duration='$(step)',hidden=false,snap=[]){
 return Object.entries(transform(p)).map(([name,v])=>{
  const d=snap.includes(name)?'0':duration;
  return`${d.includes('$')?'$':''}data merge entity @e[tag=rlk_pm,tag=rlk_pm_${name},limit=1] {interpolation_duration:${d},start_interpolation:0,transformation:${nbt(hidden?{...v,s:[0,0,0]}:v)}}`;
 }).join('\n');
}
// Gold sparkle particles for drawing/sheathing. Display translations are ^left ^up ^forward from the
// feet in the rig's yaw frame, so a transformed weapon point can be used directly.
const GOLD='minecraft:dust{color:[1.0,0.84,0.38],scale:0.55}';
const coord=x=>{const r=Math.round(x*1000)/1000;return Object.is(r,-0)||r===0?'0':String(r);};
const local=v=>`^${coord(v[0])} ^${coord(v[1])} ^${coord(v[2])}`;
const handSpark=v=>[`particle ${GOLD} ${local(v.t)} 0.1 0.12 0.1 0 8`,`particle minecraft:end_rod ${local(v.t)} 0.05 0.08 0.05 0.01 2`];
function backSpark(v,weapon){
 // Points along the model's +Y axis (grip [8,8,8]) as placed by the back mount.
 const[lo,hi]=weaponSpan[weapon]||[0,16],points=[];
 for(let i=0;i<=6;i++)points.push(add(v.t,rot(v.q,[0,v.s[1]*((lo+(hi-lo)*i/6)-8)/16,0])));
 return[...points.map(point=>`particle ${GOLD} ${local(point)} 0.04 0.05 0.04 0 2`),`particle minecraft:end_rod ${local(points[3])} 0.06 0.25 0.06 0.01 2`];
}
function weaponLines(weapon){
 const light=glowing.has(weapon)?'data merge entity @e[tag=rlk_pm_weapon,limit=1] {brightness:{block:15,sky:15}}':'data remove entity @e[tag=rlk_pm_weapon,limit=1] brightness';
 return`data modify entity @e[tag=rlk_pm_weapon,limit=1] item set value {id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:player_motion/weapons/${weapon}"}}\n${light}`;
}
function spawnLines(char,pose,weapon,hidden=false){
 const values=transform(pose);
 if(hidden)for(const value of Object.values(values))value.s=[0,0,0];
 return parts.map(name=>{
 const item=name==='weapon'?`rlk:player_motion/weapons/${weapon}`:`rlk:player_motion/${char}/${name}`;
 return`summon minecraft:item_display ~ ~ ~ {Tags:["rlk_view","rlk_pet","rlk_pm","rlk_pm_${name}"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:1.5f,width:8f,height:6f,shadow_radius:0f,${name==='weapon'&&glowing.has(weapon)?'brightness:{block:15,sky:15},':''}transformation:${nbt(values[name])},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${item}"}}}`;
 }).join('\n')+'\nexecute rotated as @s rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0\n';
}
// Clip-level weapon_state: "drawn" (default; starting it draws instantly), "sheathed" (weapon on the back for
// the whole clip unless frames change it; a drawn weapon is quick-stowed first; dash) or "sheathe" (the put-away
// clip: starts with the weapon in hand and must end with weapon_attach "back"). Per-frame weapon_attach
// "hand"|"back"|"world" is sticky like hidden. A change at t>0 snaps the weapon (interpolation 0) and, through
// sheath/clip_state, sets pmSheath (back 1, hand 0 + re-armed delay; world keeps the state). Between two keys
// whose attach differs the weapon fields hold the earlier key (the body still blends), so a sparse key gap never
// drifts the weapon toward the other frame. A frame with "weapon_snap":true (not sticky) also snaps the weapon on
// its tick, for authored pops such as a crescent appearing at full width.
const weaponStates=['drawn','sheathed','sheathe'];
const weaponFields=['weapon','weapon_shift','weapon_scale'];
const clipStates=[];
function compileClip(char,name,clip){
 if(!Number.isInteger(clip.length)||clip.length<1)throw new Error(`Invalid clip length ${char}/${name}`);
 const info=characters[char],state=clip.weapon_state||'drawn';
 if(!weaponStates.includes(state))throw new Error(`Invalid weapon_state "${state}": ${char}/${name}`);
 let prev=neutral(),weapon=clip.weapon||info.weapon,hidden=false,attach=state==='sheathed'?'back':'hand';
 const keys=clip.frames.map(frame=>{
  prev={...prev,...frame.pose};weapon=frame.weapon||weapon;hidden=frame.hidden??hidden;attach=frame.weapon_attach??attach;
  if(!(attach in attachIds))throw new Error(`Invalid weapon_attach "${attach}": ${char}/${name} tick ${frame.tick}`);
  if(frame.weapon_snap!==undefined&&typeof frame.weapon_snap!=='boolean')throw new Error(`weapon_snap must be true or false: ${char}/${name} tick ${frame.tick}`);
  return{tick:frame.tick,pose:structuredClone(prev),weapon,hidden,attach,snap:frame.weapon_snap===true};
 }).sort((a,b)=>a.tick-b.tick);
 if(keys[0]?.tick!==0)throw new Error(`First frame must be tick 0: ${char}/${name}`);
 const sample=t=>{
  let a=keys[0],b=a;for(let i=0;i<keys.length;i++){if(keys[i].tick<=t)a=keys[i];if(keys[i].tick>t){b=keys[i];break;}b=a;}
  const fraction=b.tick===a.tick?0:(t-a.tick)/(b.tick-a.tick),pose={},hold=a.attach!==b.attach;
  for(const field of Object.keys(neutral()))pose[field]=lerp(a.pose[field],b.pose[field],hold&&weaponFields.includes(field)?0:fraction);
  return{pose,weapon:a.weapon,hidden:a.hidden,attach:a.attach};
 };
 if(state==='sheathe'&&sample(clip.length).attach!=='back')throw new Error(`${char}/${name}: a "sheathe" clip must end with weapon_attach "back".`);
 // mount: the model whose back mount applies. Sheathed and put-away clips show the loco/weapon variant (mounted
 // like the default model) until a frame switches the model.
 const posed=(current,mount=current.weapon)=>rigPose(char,current.pose,current.attach,mount);
 const base=`clips/${char}/${name}`,dispatch=[];
 let lastWeapon,lastAttach=keys[0].attach,switched=state==='drawn';
 for(let t=0;t<=clip.length;t++){
  const current=sample(t),changed=t>0&&current.attach!==lastAttach,snapKey=keys.some(key=>key.tick===t&&key.snap);
  // Drawn clips set their model. The dash, sheathed and put-away clips keep whatever loco/weapon shows
  // (spear or infused scythe, sword or cryo sword) unless a later frame switches the model.
  const swap=state==='drawn'?current.weapon!==lastWeapon:t>0&&current.weapon!==lastWeapon;
  switched||=swap;
  const mount=switched?current.weapon:info.weapon;
  const lines=[`# ${char} / ${name}: authored animation tick ${t}`,poseLines(posed(current,mount),'$(step)',current.hidden,changed||snapKey?['weapon']:[])];
  if(swap)lines.push(weaponLines(current.weapon));
  if(changed){
   // Sparkle along the full-size weapon: put-away clips usually ramp weapon_scale to 0 around this tick.
   const placed=transform(posed({...current,pose:{...current.pose,weapon_scale:[1,1,1]}},mount)).weapon;
   lines.push(`# weapon_attach ${lastAttach} -> ${current.attach}: snap (no interpolation across the change)`,
    `scoreboard players set @s pmWAt ${attachIds[current.attach]}`,'scoreboard players set #pmSnapW tmp 1',
    ...(current.hidden?[]:current.attach==='back'?backSpark(placed,mount):current.attach==='hand'?handSpark(placed):[]));
   if(current.attach!=='world')clipStates.push({char,name,tick:t,attach:current.attach});
  }else if(snapKey)lines.push('# weapon_snap: the weapon jumps to this pose (also after a later pose of the same tick)','scoreboard players set #pmSnapW tmp 1');
  lastWeapon=current.weapon;lastAttach=current.attach;fn(`${base}/pose/${t}`,lines.join('\n'));
  dispatch.push(`execute if score @s pmTick matches ${t} run function rlk:char/motion/${base}/pose/${t} with storage rlk:player_motion active`);
 }
 fn(`${base}/pose`,dispatch.join('\n'));
 // A respawn inside a sheathed or put-away clip restores the loco weapon variant too.
 fn(`${base}/spawn`,spawnLines(char,posed(keys[0],state==='drawn'?keys[0].weapon:info.weapon),keys[0].weapon,keys[0].hidden)+(state==='drawn'?'':'scoreboard players set @s pmWeapon -1\nfunction rlk:char/motion/loco/weapon\n'));
 const normal=/^(physical|infused)_/.test(name);
 // The put-away clip keeps the avatar's facing (an idle character does not turn to the camera).
 const locked=name.startsWith('burst')||name==='dash'||state==='sheathe',yaw=state==='sheathe'?'@e[tag=rlk_pm_basis,limit=1]':'@s';
 const attach0=keys[0].attach,snap0=[`execute unless score @s pmWAt matches ${attachIds[attach0]} run function rlk:char/motion/sheath/snap`,`scoreboard players set @s pmWAt ${attachIds[attach0]}`];
 const hand0=transform(posed(sample(0))).weapon;
 const weaponStart={
  drawn:['# Drawn: instant draw (snap, no flight) with a gold sparkle at the hand unless it was already drawn',
   '# (from the back, or out of the put-away clip where it may be dissolved or floating).',...snap0,
   ...(clip.draw_fx===false||attach0!=='hand'?[]:[`execute unless score @s pmSheath matches 0 if entity @e[tag=rlk_pm_weapon] at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 positioned ${local(hand0.t)} run function rlk:char/motion/sheath/fx_hand`]),
   'function rlk:char/motion/sheath/draw'],
  sheathed:['# Sheathed: the weapon stays on the back (quick stow from the position marked before frame zero if it was',
   '# drawn); loco/weapon picks the variant.',...snap0,
   'function rlk:char/motion/sheath/stow_marked','function rlk:char/motion/loco/weapon'],
  sheathe:['# Put-away clip: weapon still in the hand until its weapon_attach "back" frame.',...snap0,
   'scoreboard players set @s pmSheath 2','function rlk:char/motion/loco/weapon']
 }[state];
 fn(`${base}/start`,[
  '# @s player. Existing avatar remains the gameplay body.',
  'function rlk:char/motion/release',
  'scoreboard players set @s pmBlend 0',
  'scoreboard players set @s pmWeapon -1',
  'scoreboard players set @s pmActive 1','scoreboard players set @s pmTick 0',`scoreboard players set @s pmLen ${clip.length}`,`scoreboard players set @s pmChar ${info.id}`,
  'scoreboard players set @s pmSpeed 100',...(normal?['execute if score @s atkSpeed matches 1.. run scoreboard players operation @s pmSpeed = @s atkSpeed']:[]),
  ...(normal&&clip.playback_rate&&clip.playback_rate!==100?[
   `scoreboard players set #pmRate tmp ${clip.playback_rate}`,
   'scoreboard players operation @s pmSpeed *= #pmRate tmp',
   'scoreboard players operation @s pmSpeed /= #100 tmp'
  ]:[]),
  'execute if score @s pmSpeed matches ..24 run scoreboard players set @s pmSpeed 25','execute if score @s pmSpeed matches 501.. run scoreboard players set @s pmSpeed 500',
  'scoreboard players set @s pmAcc 0','scoreboard players set @s pmStep 99','scoreboard players operation @s pmStep += @s pmSpeed','scoreboard players operation @s pmStep /= @s pmSpeed',
  `data modify storage rlk:player_motion active set value {char:"${char}",clip:"${name}",step:1,loop:${clip.loop?'1b':'0b'},lockedYaw:${locked?'1b':'0b'}}`,
  'execute store result storage rlk:player_motion active.step int 1 run scoreboard players get @s pmStep',
  ...(locked?[
   'execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_pet","rlk_pm_basis"]}',
   `execute at @e[tag=rlk_body,limit=1] rotated as ${state==='sheathe'?'@e[tag=rlk_av,limit=1]':'@s'} rotated ~ 0 run tp @e[tag=rlk_pm_basis,limit=1] ~ ~ ~ ~ 0`
  ]:[]),
  'execute unless score @s pmRigChar = #charN tmp run kill @e[tag=rlk_pm]',
  `execute if entity @e[tag=rlk_av,limit=1] unless entity @e[tag=rlk_pm] at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/${base}/spawn`,
  'execute if entity @e[tag=rlk_pm] run scoreboard players set @s pmVisible 1',
  'scoreboard players operation @s pmRigChar = #charN tmp',
  ...(state==='sheathed'?['# Where a drawn weapon is before frame zero moves it to the back (the stow sparkle).',
   'execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] run function rlk:char/motion/sheath/mark']:[]),
  '# Reuse the displayed last pose when chaining an attack; interpolate into frame zero.',
  'data modify storage rlk:player_motion active.step set value 2',
  `execute if entity @e[tag=rlk_pm] run function rlk:char/motion/${base}/pose/0 with storage rlk:player_motion active`,
  'execute store result storage rlk:player_motion active.step int 1 run scoreboard players get @s pmStep',
  `execute at @e[tag=rlk_av,limit=1] rotated as ${yaw} rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0`,
  ...weaponStart,
  'execute if entity @e[tag=rlk_av,limit=1] run function rlk:char/motion/hide_avatar',
  `execute at @e[tag=rlk_body,limit=1] rotated as ${yaw} rotated ~ 0 run function rlk:char/motion/${char}_fx/${name}`,
  `execute at @e[tag=rlk_body,limit=1] rotated as ${yaw} rotated ~ 0 run function rlk:char/motion/event`,
  'return 1'
 ].join('\n'));
 if(normal){
  // Normal-attack timing for combat/request (M/combat/config/<char>/<clip>): pmStrike, pmSecond and pmThird are
  // the authored hit ticks (up to three timeline hits), pmChain the next-input tick. All in authored ticks.
  const hits=clip.hit_ticks||[];
  if(!hits.length||hits.length>3||!hits.every(t=>Number.isInteger(t)&&t>=0&&t<=clip.length)||hits.some((t,i)=>i&&t<=hits[i-1]))
   throw new Error(`${char}/${name}: a normal clip needs 1-3 increasing integer hit_ticks within 0..length.`);
  if(!Number.isInteger(clip.chain_tick)||clip.chain_tick<hits.at(-1))
   throw new Error(`${char}/${name}: chain_tick must be an integer >= the last hit tick (an earlier next input would drop a pending hit).`);
  fn(`combat/config/${char}/${name}`,[`# Generated by build_player_rig.mjs from ${char}/${name} hit_ticks/chain_tick.`,
   ...['pmStrike','pmSecond','pmThird'].map((o,i)=>`scoreboard players set @s ${o} ${hits[i]??0}`),`scoreboard players set @s pmChain ${clip.chain_tick}`].join('\n'));
 }
 const {frames,fx,...metadata}=clip;
 return{...metadata,char,name,length:clip.length,normal,weapon:clip.weapon||info.weapon};
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
 fn('apply','$execute if entity @e[tag=rlk_pm] run function rlk:char/motion/clips/$(char)/$(clip)/pose\nfunction rlk:char/motion/sheath/clip_state\n$function rlk:char/motion/$(char)_fx/$(clip)\nfunction rlk:char/motion/event');
}
for(const[char,info]of Object.entries(characters))bodyModels(char,info.skin);
weaponModels();runtime();
const manifest=[];
for(const[char,data]of Object.entries(motionData))for(const[name,clip]of Object.entries(data.clips))manifest.push(compileClip(char,name,clip));
// Sheath state from weapon_attach changes at t>0, run by apply on every authored tick (also in first
// person, where the pose files do not run). The visual snap and sparkle live in the pose files.
fn('sheath/clip_state',['# Generated by build_player_rig.mjs from per-frame weapon_attach changes (@s player, from apply).',
 ...clipStates.map(({char,name,tick,attach})=>`execute if score @s pmTick matches ${tick} if data storage rlk:player_motion active{char:"${char}",clip:"${name}"} run ${attach==='back'?'scoreboard players set @s pmSheath 1':'function rlk:char/motion/sheath/draw'}`)].join('\n'));
const atlasPath=path.join(rpRoot,'assets/minecraft/atlases/items.json');
const atlas=fs.existsSync(atlasPath)?JSON.parse(fs.readFileSync(atlasPath,'utf8')):{sources:[]};
for(const block of blocks){const sprite='rlk:player_motion/'+block;atlas.sources=atlas.sources.filter(s=>s.sprite!==sprite);atlas.sources.push({type:'minecraft:single',resource:'minecraft:block/'+block,sprite});}
for(const info of Object.values(characters))if(!atlas.sources.some(s=>s.type==='minecraft:single'&&s.resource==='rlk:skin/'+info.skin&&!s.sprite))atlas.sources.push({type:'minecraft:single',resource:'rlk:skin/'+info.skin});
buildLocomotion({fn,poseLines,spawnLines,weaponLines,neutral,lerp,characters,here,rigPose,transform,handSpark,backSpark,arr});
// Dash: player/dash_go calls this; a character with a "dash" clip plays it (gameplay moves the body).
// The clip's yaw is locked (like a burst) and its basis turned to the dash direction set by
// player/dash_dir (dashUX/dashUZ, unit x100), so a sideways or backward dash leans that way.
fn('dash',['# @s = player, from player/dash_go: play the character dash clip when it has one.',...Object.entries(characters).filter(([c])=>motionData[c].clips.dash).map(([c,info])=>`execute if score #charN tmp matches ${info.id} run function rlk:char/motion/start {char:"${c}",clip:"dash"}`),
 'execute unless data storage rlk:player_motion active{clip:"dash"} run return 0',
 'execute store result storage rlk:player_motion face.dx double 0.01 run scoreboard players get @s dashUX',
 'execute store result storage rlk:player_motion face.dz double 0.01 run scoreboard players get @s dashUZ',
 'function rlk:char/motion/dash_face with storage rlk:player_motion face'].join('\n'));
fn('dash_face',['# Turn the dash clip basis (and the rig) toward the dash direction.',
 '$execute as @e[tag=rlk_pm_basis,limit=1] at @s run tp @s ~ ~ ~ facing ~$(dx) ~ ~$(dz)',
 'execute at @e[tag=rlk_av,limit=1] rotated as @e[tag=rlk_pm_basis,limit=1] rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0'].join('\n'));
json(atlasPath,atlas);json(path.join(here,'player_motion/compiled_clips.json'),manifest);
console.log(`Built articulated combat avatars and ${manifest.length} clips.`);
