// Continuous non-combat avatar poses and interruptible quaternion recovery.
// Invoked by build_player_rig.mjs; gameplay cooldowns and attack events stay separate.
import fs from 'node:fs';
import path from 'node:path';
// Sheathed/drawn weapon state (all rig characters):
//  pmSheath 0 drawn (in hand) | 1 sheathed (on the back) | 2 put-away clip running; unset counts as 1
//  pmShT    countdown to putting the weapon away; runs only while drawn and no clip is active
//  pmLocS   sheath state the current loco cycle was begun with (a change restarts the cycle)
//  pmShFx   quick-stow visual: weapon hidden, then it re-forms on the back (<char>.json sheath.grow)
//  pmWAt    weapon attach currently displayed (0 hand, 1 back, 2 world); a change snaps the weapon
//  pmWModel weapon model currently displayed (build_player_rig.mjs model id); a drawn clip of another model snaps
export const locomotionObjectives=['pmVisible','pmRigChar','pmLocMode','pmWantMode','pmLocT','pmLocAcc','pmLocSpeed','pmBlend','pmPX','pmPZ','pmPosValid','pmWeapon','pmWantW','pmSheath','pmShT','pmLocS','pmShFx','pmWAt','pmWModel'];
// Ticks a drawn weapon stays out after the last drawn clip (#pmShDelay tmp); <char>.json sheath.delay overrides.
const SHEATH_DELAY=100;
// Ticks of the quick-stow visual (pmShFx): the weapon stays hidden, then re-forms on the back in the last ticks.
const STOW_FX=8;
export function buildLocomotion({fn,poseLines,spawnLines,weaponLines,neutral,lerp,characters,here,rigPose,transform,handSpark,backSpark,arr}){
 const source=JSON.parse(fs.readFileSync(path.join(here,'player_motion/locomotion.json'),'utf8'));
 const modes=['idle','walk','run','air'];
 for(const char of Object.keys(source.characters))if(!characters[char])throw new Error(`locomotion.json: "${char}" is not in build_player_rig.mjs characters.`);
 const backRest={};
 for(const [char,info] of Object.entries(characters)){
  const motions=source.characters[char];
  if(!motions)throw new Error(`locomotion.json: characters.${char} is missing.`);
  // Drawn sets <mode> hold the weapon in hand; sheathed sets <mode>_s (authored, else the drawn poses)
  // hang it on the back. Both share the drawn cadence.
  for(const mode of modes)for(const sheathed of [false,true]){
   const set=sheathed?mode+'_s':mode,clip=sheathed?motions[set]??motions[mode]:motions[mode];
   if(!clip)throw new Error(`locomotion.json: characters.${char}.${mode} is missing.`);
   const posed=pose=>sheathed?rigPose(char,pose,'back'):rigPose(char,pose,'hand',info.weapon,{scythe_loco:info.scytheLoco});
   let prev=neutral();
   const keys=clip.frames.map(f=>{prev={...prev,...f.pose};return{tick:f.tick,pose:structuredClone(prev)};});
   const sample=t=>{let a=keys[0],b=a;for(const k of keys){if(k.tick<=t)a=k;if(k.tick>t){b=k;break;}b=a;}const u=b.tick===a.tick?0:(t-a.tick)/(b.tick-a.tick);return Object.fromEntries(Object.keys(neutral()).map(k=>[k,lerp(a.pose[k],b.pose[k],u)]));};
   const dispatch=[];
   // Omit repeated endpoint; wrapping to zero keeps the loop cadence exact.
   for(let t=0;t<clip.length;t++){
    fn(`loco/${char}/${set}/${t}`,poseLines(posed(sample(t))));
    dispatch.push(`execute if score @s pmLocT matches ${t} run function rlk:char/motion/loco/${char}/${set}/${t} with storage rlk:player_motion loco`);
   }
   fn(`loco/${char}/${set}/pose`,dispatch.join('\n'));
   fn(`loco/${char}/${set}/advance`,[
    `execute if score @s pmLocT matches ${clip.length}.. run scoreboard players set @s pmLocT 0`,
    `function rlk:char/motion/loco/${char}/${set}/pose`
   ].join('\n'));
   if(mode!=='idle')continue;
   fn(`loco/${char}/${sheathed?'spawn_s':'spawn'}`,spawnLines(char,posed(keys[0].pose),info.weapon));
   if(sheathed)backRest[char]=transform(posed(keys[0].pose)).weapon;
  }
 }
 const core=['pmActive','pmTick','pmLen','pmChar','pmSpeed','pmAcc','pmStep'];
 fn('init',[...core.concat(locomotionObjectives).map(o=>`scoreboard objectives add ${o} dummy`),`scoreboard players set #pmShDelay tmp ${SHEATH_DELAY}`,'execute as @a[tag=player] run function rlk:char/motion/stop','kill @e[tag=rlk_pm]','kill @e[tag=rlk_pm_basis]'].join('\n'));
 fn('release',[
  '# End the old action while preserving all display transforms for interpolation.',
  'execute if score @s pmActive matches 1 run function rlk:char/motion/control/cancel',
  'execute if data storage rlk:player_motion active.clip run function rlk:char/motion/audio/stop with storage rlk:player_motion active',
  'function rlk:char/motion/control/unlock',
  ...['pmActive','pmTick','pmAcc','pmAtkPending'].map(o=>`scoreboard players set @s ${o} 0`),
  'kill @e[tag=rlk_pm_basis]','data remove storage rlk:player_motion active'
 ].join('\n'));
 fn('stop',[
  '# Hard cleanup for lifecycle changes; normal animation endings use finish.',
  'function rlk:char/motion/release','kill @e[tag=rlk_pm]',
  ...['pmVisible','pmPosValid','pmBlend','pmLocT','pmLocAcc'].map(o=>`scoreboard players set @s ${o} 0`),
  'scoreboard players set @s pmLocMode -1','scoreboard players set @s pmWeapon -1','scoreboard players set @s pmWModel 0',
  '# Every lifecycle reset (death, map, selection space, view, character switch, reload) leaves the weapon sheathed.',
  'scoreboard players set @s pmSheath 1','scoreboard players set @s pmShT 0','scoreboard players set @s pmShFx 0','scoreboard players set @s pmLocS -1','scoreboard players set @s pmWAt -1',
  'execute if entity @e[tag=rlk_av,limit=1] run effect clear @e[tag=rlk_av,limit=1] minecraft:invisibility',
  'execute if entity @e[tag=rlk_av,limit=1] run item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand from entity @s hotbar.0',
  'execute if entity @e[tag=rlk_av,limit=1] run function rlk:view/av_unwrap',
  'execute if score #charN tmp matches 7..8 run item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand with minecraft:air'
 ].join('\n'));
 fn('cleanup','execute if score @s pmActive matches 1 run function rlk:char/motion/stop\nexecute if score @s pmVisible matches 1 run function rlk:char/motion/stop');
 fn('finish',[
  'function rlk:char/motion/release',
  'execute unless entity @e[tag=rlk_av,limit=1] run return 0',
  'function rlk:char/motion/loco/context',
  'function rlk:char/motion/loco/begin'
 ].join('\n'));
 fn('tick',[
  '# Combat active state remains separate from persistent locomotion visibility.',
  `execute ${Object.values(characters).map(info=>info.id).sort((a,b)=>a-b).map(id=>`unless score #charN tmp matches ${id}`).join(' ')} run return run function rlk:char/motion/cleanup`,
  ...['dead matches 1','vMap matches 1','pkMode matches 1..'].map(c=>`execute if score @s ${c} run return run function rlk:char/motion/cleanup`),
  'execute unless entity @e[tag=rlk_body,limit=1] run return run function rlk:char/motion/cleanup',
  'execute if score @s pmActive matches 1 unless score @s pmChar = #charN tmp run function rlk:char/motion/stop',
  'execute if score @s pmVisible matches 1 unless score @s pmRigChar = #charN tmp run function rlk:char/motion/stop',
  'execute unless entity @e[tag=rlk_av,limit=1] run kill @e[tag=rlk_pm]',
  'execute unless entity @e[tag=rlk_av,limit=1] run scoreboard players set @s pmVisible 0',
  'execute if entity @e[tag=rlk_av,limit=1] run function rlk:char/motion/loco/observe',
  '# Weapon state first (it may start the put-away clip or blend locomotion into the sheathed set).',
  'function rlk:char/motion/sheath/tick',
  '# No locomotion on the tick a clip finished (finish already posed the blend).',
  'execute store result score #pmWasActive tmp if score @s pmActive matches 1',
  'execute if score #pmWasActive tmp matches 1 run function rlk:char/motion/combat_tick',
  'execute if score #pmWasActive tmp matches 0 if entity @e[tag=rlk_av,limit=1] run function rlk:char/motion/loco/tick',
  'execute if score @s pmShFx matches 1.. run function rlk:char/motion/sheath/fx_tick',
  '# Attach changes snap even when several authored ticks (or a start and its first advance) ran this tick.',
  'execute if score #pmSnapW tmp matches 1 run function rlk:char/motion/sheath/snap_end'
 ].join('\n'));
 fn('combat_tick',[
  'execute if data storage rlk:player_motion active{lockedYaw:1b} unless entity @e[tag=rlk_pm_basis,limit=1] run return run function rlk:char/motion/finish',
  'execute if entity @e[tag=rlk_av,limit=1] unless entity @e[tag=rlk_pm] at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/respawn with storage rlk:player_motion active',
  'execute if entity @e[tag=rlk_pm] run scoreboard players set @s pmVisible 1',
  'execute if entity @e[tag=rlk_av,limit=1] run function rlk:char/motion/hide_avatar',
  'execute unless data storage rlk:player_motion active{lockedYaw:1b} at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0',
  'execute if data storage rlk:player_motion active{lockedYaw:1b} at @e[tag=rlk_av,limit=1] rotated as @e[tag=rlk_pm_basis,limit=1] rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0',
  'scoreboard players operation @s pmAcc += @s pmSpeed',
  'execute if score @s pmAcc matches 100.. unless data storage rlk:player_motion active{lockedYaw:1b} at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/advance',
  'execute if score @s pmAcc matches 100.. if data storage rlk:player_motion active{lockedYaw:1b} at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_pm_basis,limit=1] rotated ~ 0 run function rlk:char/motion/advance'
 ].join('\n'));
 fn('advance',[
  'scoreboard players remove @s pmAcc 100','scoreboard players add @s pmTick 1',
  'execute if score @s pmTick > @s pmLen if data storage rlk:player_motion active{loop:1b} run scoreboard players set @s pmTick 0',
  'execute if score @s pmTick > @s pmLen run return run function rlk:char/motion/finish',
  'function rlk:char/motion/apply with storage rlk:player_motion active',
  'execute if score @s pmActive matches 1 if score @s pmAcc matches 100.. run function rlk:char/motion/advance'
 ].join('\n'));
 fn('loco/observe',[
  '# Centiblock displacement, not requested velocity: a wall stops the gait.',
  'execute store result score #pmX tmp run data get entity @e[tag=rlk_av,limit=1] Pos[0] 100',
  'execute store result score #pmZ tmp run data get entity @e[tag=rlk_av,limit=1] Pos[2] 100',
  'scoreboard players operation #pmDX tmp = #pmX tmp','scoreboard players operation #pmDZ tmp = #pmZ tmp',
  'scoreboard players operation #pmDX tmp -= @s pmPX','scoreboard players operation #pmDZ tmp -= @s pmPZ',
  'execute unless score @s pmPosValid matches 1 run scoreboard players set #pmDX tmp 0',
  'execute unless score @s pmPosValid matches 1 run scoreboard players set #pmDZ tmp 0',
  'scoreboard players operation @s pmPX = #pmX tmp','scoreboard players operation @s pmPZ = #pmZ tmp','scoreboard players set @s pmPosValid 1',
  'scoreboard players set #pmNeg tmp -1',
  'execute if score #pmDX tmp matches ..-1 run scoreboard players operation #pmDX tmp *= #pmNeg tmp',
  'execute if score #pmDZ tmp matches ..-1 run scoreboard players operation #pmDZ tmp *= #pmNeg tmp',
  'scoreboard players operation #pmMove tmp = #pmDX tmp','scoreboard players operation #pmMove tmp > #pmDZ tmp',
  'scoreboard players operation #pmMinor tmp = #pmDX tmp','scoreboard players operation #pmMinor tmp < #pmDZ tmp',
  '# Ignore teleports; locomotion resumes from the next ordinary displacement.',
  'execute if score #pmMove tmp matches 101.. run scoreboard players set #pmMinor tmp 0',
  'execute if score #pmMove tmp matches 101.. run scoreboard players set #pmMove tmp 0',
  '# max + 3/8 min approximates distance without slowing diagonal footsteps.',
  'scoreboard players set #pmThree tmp 3','scoreboard players set #pmEight tmp 8',
  'scoreboard players operation #pmMinor tmp *= #pmThree tmp','scoreboard players operation #pmMinor tmp /= #pmEight tmp',
  'scoreboard players operation #pmMove tmp += #pmMinor tmp',
  'scoreboard players set @s pmWantMode 0',
  'execute if score #pmMove tmp matches 2.. if score #inAct view matches 1 run scoreboard players set @s pmWantMode 1',
  'execute if score @s pmWantMode matches 1 if score #sprNow view matches 1 run scoreboard players set @s pmWantMode 2',
  'execute if score @s dashMoveT matches 1.. run scoreboard players set @s pmWantMode 2',
  'execute unless data entity @e[tag=rlk_av,limit=1] {OnGround:1b} run scoreboard players set @s pmWantMode 3',
  'scoreboard players set @s pmLocSpeed 100',
  'execute if score @s pmWantMode matches 1..2 run scoreboard players operation @s pmLocSpeed = #pmMove tmp',
  'execute if score @s pmWantMode matches 1..2 run scoreboard players operation @s pmLocSpeed *= #100 tmp',
  'scoreboard players set #pmStride tmp 20','execute if score @s pmWantMode matches 2 run scoreboard players set #pmStride tmp 30',
  'execute if score @s pmWantMode matches 1..2 run scoreboard players operation @s pmLocSpeed /= #pmStride tmp',
  'execute if score @s pmLocSpeed matches ..49 run scoreboard players set @s pmLocSpeed 50',
  'execute if score @s pmLocSpeed matches 201.. run scoreboard players set @s pmLocSpeed 200'
 ].join('\n'));
 fn('loco/context',[
  ...Object.entries(characters).map(([char,info])=>`execute if score #charN tmp matches ${info.id} run data modify storage rlk:player_motion loco.char set value "${char}"`),
  ...modes.map((mode,i)=>`execute if score @s pmWantMode matches ${i} run data modify storage rlk:player_motion loco.mode set value "${mode}"`),
  'execute if score @s pmSheath matches 1 run function rlk:char/motion/loco/context_s'
 ].join('\n'));
 fn('loco/context_s',['# Sheathed locomotion: weapon on the back, relaxed empty-hand arms.',
  ...modes.map((mode,i)=>`execute if score @s pmWantMode matches ${i} run data modify storage rlk:player_motion loco.mode set value "${mode}_s"`)].join('\n'));
 fn('loco/spawn','$execute if score @s pmSheath matches 1 run return run function rlk:char/motion/loco/$(char)/spawn_s\n$function rlk:char/motion/loco/$(char)/spawn');
 fn('loco/pose','$function rlk:char/motion/loco/$(char)/$(mode)/pose');
 fn('loco/frame','$function rlk:char/motion/loco/$(char)/$(mode)/advance');
 fn('loco/begin',[
  '# Minecraft display quaternion interpolation chooses the shortest return arc.',
  'scoreboard players operation @s pmLocMode = @s pmWantMode','scoreboard players set @s pmLocT 0','scoreboard players set @s pmLocAcc 0',
  'scoreboard players set @s pmLocS 0','execute if score @s pmSheath matches 1 run scoreboard players set @s pmLocS 1',
  'scoreboard players set @s pmBlend 6','execute if score @s pmWantMode matches 1.. run scoreboard players set @s pmBlend 4',
  'execute store result storage rlk:player_motion loco.step int 1 run scoreboard players get @s pmBlend',
  'function rlk:char/motion/loco/context',
  'function rlk:char/motion/loco/pose with storage rlk:player_motion loco',
  '# Hand and back never blend into each other: the weapon snaps when the attach changes.',
  'execute unless score @s pmWAt = @s pmLocS run function rlk:char/motion/sheath/snap',
  'scoreboard players operation @s pmWAt = @s pmLocS',
  'function rlk:char/motion/loco/weapon',
  'data modify storage rlk:player_motion loco.step set value 1'
 ].join('\n'));
 fn('loco/tick',[
  'function rlk:char/motion/loco/context',
  'execute unless entity @e[tag=rlk_pm] at @e[tag=rlk_av,limit=1] run function rlk:char/motion/loco/ensure',
  'function rlk:char/motion/hide_avatar',
  '# Follow the smoothed body heading, including sideways and backward travel.',
  'execute at @e[tag=rlk_av,limit=1] rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0',
  'function rlk:char/motion/loco/weapon',
  'execute unless score @s pmLocMode = @s pmWantMode run return run function rlk:char/motion/loco/begin',
  'execute if score @s pmSheath matches 1 unless score @s pmLocS matches 1 run return run function rlk:char/motion/loco/begin',
  'execute unless score @s pmSheath matches 1 unless score @s pmLocS matches 0 run return run function rlk:char/motion/loco/begin',
  '# The displayed attach must be the cycle\'s: a clip released without finish may leave the weapon on the back or',
  '# floating, and begin snaps it instead of letting the frames glide it across the change.',
  'execute unless score @s pmWAt = @s pmLocS run return run function rlk:char/motion/loco/begin',
  'execute if score @s pmBlend matches 1.. run return run scoreboard players remove @s pmBlend 1',
  'scoreboard players set #pmInterp tmp 99','scoreboard players operation #pmInterp tmp += @s pmLocSpeed',
  'scoreboard players operation #pmInterp tmp /= @s pmLocSpeed',
  'execute store result storage rlk:player_motion loco.step int 1 run scoreboard players get #pmInterp tmp',
  'scoreboard players operation @s pmLocAcc += @s pmLocSpeed',
  'execute if score @s pmLocAcc matches 100.. run function rlk:char/motion/loco/advance'
 ].join('\n'));
 fn('loco/ensure',[
  'function rlk:char/motion/loco/spawn with storage rlk:player_motion loco',
  'scoreboard players set @s pmVisible 1','scoreboard players operation @s pmRigChar = #charN tmp',
  'scoreboard players set @s pmLocMode -1','scoreboard players set @s pmWeapon -1'
 ].join('\n'));
 fn('loco/advance',[
  'scoreboard players remove @s pmLocAcc 100','scoreboard players add @s pmLocT 1',
  'function rlk:char/motion/loco/frame with storage rlk:player_motion loco',
  'execute if score @s pmLocAcc matches 100.. run function rlk:char/motion/loco/advance'
 ].join('\n'));
 // pmWantW = 1-based index in the combined locoWeapons list; the last matching entry of the character wins.
 const weapons=[...new Set(Object.values(characters).flatMap(info=>info.locoWeapons.map(entry=>entry.weapon)))];
 fn('loco/weapon',[
  'scoreboard players set @s pmWantW 1',
  ...Object.values(characters).flatMap(info=>info.locoWeapons.map((entry,i)=>({info,entry,i})))
   // The first unconditional entry equal to the default line is redundant.
   .filter(({entry,i})=>!(i===0&&!entry.if&&weapons.indexOf(entry.weapon)===0))
   .map(({info,entry})=>`execute if score #charN tmp matches ${info.id}${entry.if?' if '+entry.if:''} run scoreboard players set @s pmWantW ${weapons.indexOf(entry.weapon)+1}`),
  'execute unless score @s pmWeapon = @s pmWantW run function rlk:char/motion/loco/weapon_set'
 ].join('\n'));
 for(const weapon of weapons)fn(`loco/weapon/${weapon}`,weaponLines(weapon));
 fn('loco/weapon_set',[
  ...weapons.map((w,i)=>`execute if score @s pmWantW matches ${i+1} run function rlk:char/motion/loco/weapon/${w}`),
  'scoreboard players operation @s pmWeapon = @s pmWantW'
 ].join('\n'));
 buildSheath({fn,characters,backRest,handSpark,backSpark,arr});
}
// Runtime of the sheathed/drawn state machine (M/sheath/*). All visuals are guarded by rlk_pm_weapon, so in
// first person (no rig) only the state changes; the held vanilla item is never touched.
function buildSheath({fn,characters,backRest,handSpark,backSpark,arr}){
 const chars=Object.entries(characters);
 const atBody='at @e[tag=rlk_pm_body,limit=1] rotated as @e[tag=rlk_pm_body,limit=1]';
 fn('sheath/tick',[
  '# @s player, every rig tick after loco/observe and before the clip or locomotion.',
  'execute unless score @s pmSheath matches 0.. run scoreboard players set @s pmSheath 1',
  '# Self-heal: a put-away state without its clip (release without finish) counts as drawn, retry in 1 s. The',
  '# locomotion cycle restarts, so loco/begin blends the body and snaps the weapon back from the clip\'s attach.',
  'execute if score @s pmSheath matches 2 unless score @s pmActive matches 1 run scoreboard players set @s pmShT 20',
  'execute if score @s pmSheath matches 2 unless score @s pmActive matches 1 run scoreboard players set @s pmLocS -1',
  'execute if score @s pmSheath matches 2 unless score @s pmActive matches 1 run scoreboard players set @s pmSheath 0',
  '# Moving during the put-away clip: quick stow and blend into sheathed locomotion.',
  'execute if score @s pmActive matches 1 if data storage rlk:player_motion active{clip:"sheathe"} unless score @s pmWantMode matches 0 run return run function rlk:char/motion/sheath/abort',
  'execute unless score @s pmSheath matches 0 run return 0',
  'execute if score @s pmActive matches 1 run return 0',
  'execute if score @s rdCam matches 1 run return 0',
  'execute if score @s pmShT matches 1.. run scoreboard players remove @s pmShT 1',
  'execute if score @s pmShT matches 1.. run return 0',
  '# Delay over: first person, moving or airborne = quick stow; idle on the ground = put-away clip.',
  'execute unless entity @e[tag=rlk_av,limit=1] run return run function rlk:char/motion/sheath/stow',
  'execute unless score @s pmWantMode matches 0 run return run function rlk:char/motion/sheath/stow',
  'function rlk:char/motion/sheath/begin'
 ].join('\n'));
 fn('sheath/begin',['# Generated: the put-away clip (clips.sheathe) when the character has one, else a quick stow.',
  ...chars.filter(([,info])=>info.hasSheathe).map(([char,info])=>`execute if score #charN tmp matches ${info.id} run return run function rlk:char/motion/start {char:"${char}",clip:"sheathe"}`),
  'function rlk:char/motion/sheath/stow'].join('\n'));
 fn('sheath/arm',['# Restart the put-away countdown (#pmShDelay ticks, or the character sheath.delay).',
  'scoreboard players operation @s pmShT = #pmShDelay tmp',
  ...chars.filter(([,info])=>Number.isInteger(info.sheath.delay)).map(([,info])=>`execute if score #charN tmp matches ${info.id} run scoreboard players set @s pmShT ${info.sheath.delay}`)].join('\n'));
 fn('sheath/draw',['# Drawn clip start or weapon_attach "hand" (the start already snapped the weapon and sparkled).',
  'scoreboard players set @s pmSheath 0','scoreboard players set @s pmShFx 0','function rlk:char/motion/sheath/arm'].join('\n'));
 // Quick stow. The sparkle is where the weapon is (in the hand mid-stride, floating in a put-away clip), read
 // from its display translation: ^left ^up ^forward from the feet in the rig yaw, like local() points.
 fn('sheath/stow',['# Quick stow from where the weapon is now (sheath/tick at the end of the delay, sheath/abort).',
  'execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] run function rlk:char/motion/sheath/mark',
  'function rlk:char/motion/sheath/stow_marked'].join('\n'));
 fn('sheath/mark',['# Grip position of the displayed weapon for the stow sparkle (sheathed clip starts mark before frame zero).',
  ...['x','y','z'].map((axis,i)=>`execute store result storage rlk:player_motion spark.${axis} double 0.001 run data get entity @e[tag=rlk_pm_weapon,limit=1] transformation.translation[${i}] 1000`)].join('\n'));
 fn('sheath/stow_marked',['# Gold sparkle at the marked position, the weapon vanishes, then re-forms on the back (sheath/fx_tick).',
  `execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] run scoreboard players set @s pmShFx ${STOW_FX}`,
  'execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] run data merge entity @e[tag=rlk_pm_weapon,limit=1] {start_interpolation:0,interpolation_duration:0,transformation:{scale:[0f,0f,0f]}}',
  'execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] run function rlk:char/motion/sheath/spark with storage rlk:player_motion spark',
  `execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] at @e[tag=rlk_pm_body,limit=1] run playsound minecraft:item.armor.equip_iron player @s ~ ~1 ~ 0.35 1.5 0`,
  'scoreboard players set @s pmSheath 1','scoreboard players set @s pmShT 0'].join('\n'));
 fn('sheath/spark',`$execute ${atBody} positioned ^$(x) ^$(y) ^$(z) run function rlk:char/motion/sheath/fx_hand`);
 fn('sheath/abort',['# Moving during the put-away clip.','function rlk:char/motion/sheath/stow','function rlk:char/motion/finish'].join('\n'));
 fn('sheath/snap',['# The weapon jumps to its new attach this tick (no hand/back/world interpolation); repeated at the end of motion/tick.',
  'execute if entity @e[tag=rlk_pm_weapon] run data merge entity @e[tag=rlk_pm_weapon,limit=1] {interpolation_duration:0,start_interpolation:0}',
  'scoreboard players set #pmSnapW tmp 1'].join('\n'));
 fn('sheath/snap_end',['# End of motion/tick: re-apply the snap after the last pose of the tick.',
  'execute if entity @e[tag=rlk_pm_weapon] run data merge entity @e[tag=rlk_pm_weapon,limit=1] {interpolation_duration:0,start_interpolation:0}',
  'scoreboard players set #pmSnapW tmp 0'].join('\n'));
 // Re-form on the back (<char>.json sheath.grow): after the hidden ticks, one step per tick, each a scale [x,y,z]
 // relative to the back mount, or {"scale":[x,y,z],"snap":true} to jump there without interpolation. The pose's
 // full scale follows on the next tick. Default: uniform 40 % then 75 %. A crescent that would sweep through the
 // head while partly wide (Arlecchino) grows as a full-length sliver first and then snaps to its width.
 const grows=Object.fromEntries(chars.map(([char,info])=>{
  const steps=(info.sheath.grow??[[.4,.4,.4],[.75,.75,.75]]).map(step=>Array.isArray(step)?{scale:step}:step);
  if(!steps.length||steps.length>STOW_FX-2||steps.some(step=>!Array.isArray(step.scale)||step.scale.length!==3||!step.scale.every(Number.isFinite)))
   throw new Error(`${char}.json sheath.grow: 1-${STOW_FX-2} steps, each [x,y,z] or {"scale":[x,y,z],"snap":true}.`);
  return[char,steps];
 }));
 fn('sheath/fx_tick',['# After the pose of this tick: keep the stowed weapon hidden, then re-form it on the back (sheath.grow), with a',
  '# gold line along it on the first step.',
  'scoreboard players remove @s pmShFx 1',
  ...chars.flatMap(([char,info])=>{
   const steps=grows[char],when=fx=>`execute if score @s pmShFx matches ${fx} if score #charN tmp matches ${info.id} if entity @e[tag=rlk_pm_weapon]`;
   return[`${when(steps.length+1+'..')} run data merge entity @e[tag=rlk_pm_weapon,limit=1] {start_interpolation:0,interpolation_duration:0,transformation:{scale:[0f,0f,0f]}}`,
    ...steps.map((step,i)=>`${when(steps.length-i)} run data merge entity @e[tag=rlk_pm_weapon,limit=1] {start_interpolation:0,interpolation_duration:${step.snap?0:1},transformation:{scale:${arr(backRest[char].s.map((x,k)=>x*step.scale[k]))}}}`),
    `${when(steps.length)} ${atBody} run function rlk:char/motion/sheath/fx_back`];
  })].join('\n'));
 fn('sheath/fx_hand',['# Gold sparkle at the hand (positioned by the caller).',...handSpark({t:[0,0,0]}).map(line=>line.replace('^0 ^0 ^0','~ ~ ~'))].join('\n'));
 fn('sheath/fx_back',['# Gold line along the weapon hanging on the back (idle sheathed pose; ^ from the feet, rig yaw).',
  ...chars.flatMap(([char,info])=>backSpark(backRest[char],info.weapon).map(line=>`execute if score #charN tmp matches ${info.id} run ${line}`))].join('\n'));
}

