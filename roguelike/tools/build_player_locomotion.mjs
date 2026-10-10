// Continuous non-combat avatar poses and interruptible quaternion recovery.
// Invoked by build_player_rig.mjs; gameplay cooldowns and attack events stay separate.
import fs from 'node:fs';
import path from 'node:path';
export const locomotionObjectives=['pmVisible','pmRigChar','pmLocMode','pmWantMode','pmLocT','pmLocAcc','pmLocSpeed','pmBlend','pmPX','pmPZ','pmPosValid','pmWeapon','pmWantW'];
export function buildLocomotion({fn,poseLines,spawnLines,weaponLines,neutral,lerp,characters,here}){
 const source=JSON.parse(fs.readFileSync(path.join(here,'player_motion/locomotion.json'),'utf8'));
 const modes=['idle','walk','run','air'];
 for(const [char,motions] of Object.entries(source.characters))for(const [mode,clip] of Object.entries(motions)){
  let prev=neutral();
  const keys=clip.frames.map(f=>{prev={...prev,...f.pose};return{tick:f.tick,pose:structuredClone(prev)};});
  const sample=t=>{let a=keys[0],b=a;for(const k of keys){if(k.tick<=t)a=k;if(k.tick>t){b=k;break;}b=a;}const u=b.tick===a.tick?0:(t-a.tick)/(b.tick-a.tick);return Object.fromEntries(Object.keys(neutral()).map(k=>[k,lerp(a.pose[k],b.pose[k],u)]));};
  const dispatch=[];
  // Omit repeated endpoint; wrapping to zero keeps the loop cadence exact.
  for(let t=0;t<clip.length;t++){
   fn(`loco/${char}/${mode}/${t}`,poseLines({...sample(t),scythe_loco:char==='arle'}));
   dispatch.push(`execute if score @s pmLocT matches ${t} run function rlk:char/motion/loco/${char}/${mode}/${t} with storage rlk:player_motion loco`);
  }
  fn(`loco/${char}/${mode}/pose`,dispatch.join('\n'));
  fn(`loco/${char}/${mode}/advance`,[
   `execute if score @s pmLocT matches ${clip.length}.. run scoreboard players set @s pmLocT 0`,
   `function rlk:char/motion/loco/${char}/${mode}/pose`
  ].join('\n'));
  if(mode==='idle')fn(`loco/${char}/spawn`,spawnLines(char,{...keys[0].pose,scythe_loco:char==='arle'},characters[char].weapon));
 }
 const core=['pmActive','pmTick','pmLen','pmChar','pmSpeed','pmAcc','pmStep'];
 fn('init',[...core.concat(locomotionObjectives).map(o=>`scoreboard objectives add ${o} dummy`),'execute as @a[tag=player] run function rlk:char/motion/stop','kill @e[tag=rlk_pm]','kill @e[tag=rlk_pm_basis]'].join('\n'));
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
  'scoreboard players set @s pmLocMode -1','scoreboard players set @s pmWeapon -1',
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
  'execute unless score #charN tmp matches 3 unless score #charN tmp matches 5 run return run function rlk:char/motion/cleanup',
  ...['dead matches 1','vMap matches 1','pkMode matches 1..'].map(c=>`execute if score @s ${c} run return run function rlk:char/motion/cleanup`),
  'execute unless entity @e[tag=rlk_body,limit=1] run return run function rlk:char/motion/cleanup',
  'execute if score @s pmActive matches 1 unless score @s pmChar = #charN tmp run function rlk:char/motion/stop',
  'execute if score @s pmVisible matches 1 unless score @s pmRigChar = #charN tmp run function rlk:char/motion/stop',
  'execute unless entity @e[tag=rlk_av,limit=1] run kill @e[tag=rlk_pm]',
  'execute unless entity @e[tag=rlk_av,limit=1] run scoreboard players set @s pmVisible 0',
  'execute if entity @e[tag=rlk_av,limit=1] run function rlk:char/motion/loco/observe',
  'execute if score @s pmActive matches 1 run return run function rlk:char/motion/combat_tick',
  'execute if entity @e[tag=rlk_av,limit=1] run function rlk:char/motion/loco/tick'
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
  'execute if score #charN tmp matches 5 run data modify storage rlk:player_motion loco.char set value "arle"',
  'execute if score #charN tmp matches 3 run data modify storage rlk:player_motion loco.char set value "skirk"',
  ...modes.map((mode,i)=>`execute if score @s pmWantMode matches ${i} run data modify storage rlk:player_motion loco.mode set value "${mode}"`)
 ].join('\n'));
 fn('loco/spawn','$function rlk:char/motion/loco/$(char)/spawn');
 fn('loco/pose','$function rlk:char/motion/loco/$(char)/$(mode)/pose');
 fn('loco/frame','$function rlk:char/motion/loco/$(char)/$(mode)/advance');
 fn('loco/begin',[
  '# Minecraft display quaternion interpolation chooses the shortest return arc.',
  'scoreboard players operation @s pmLocMode = @s pmWantMode','scoreboard players set @s pmLocT 0','scoreboard players set @s pmLocAcc 0',
  'scoreboard players set @s pmBlend 6','execute if score @s pmWantMode matches 1.. run scoreboard players set @s pmBlend 4',
  'execute store result storage rlk:player_motion loco.step int 1 run scoreboard players get @s pmBlend',
  'function rlk:char/motion/loco/context',
  'function rlk:char/motion/loco/pose with storage rlk:player_motion loco',
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
 fn('loco/weapon',[
  'scoreboard players set @s pmWantW 1',
  'execute if score #charN tmp matches 5 if score @s arM matches 1.. run scoreboard players set @s pmWantW 2',
  'execute if score #charN tmp matches 3 run scoreboard players set @s pmWantW 3',
  'execute if score #charN tmp matches 3 if score @s skM matches 1.. run scoreboard players set @s pmWantW 4',
  'execute unless score @s pmWeapon = @s pmWantW run function rlk:char/motion/loco/weapon_set'
 ].join('\n'));
 const weapons=['spear','scythe','sword','cryo_sword'];
 for(const weapon of weapons)fn(`loco/weapon/${weapon}`,weaponLines(weapon));
 fn('loco/weapon_set',[
  ...weapons.map((w,i)=>`execute if score @s pmWantW matches ${i+1} run function rlk:char/motion/loco/weapon/${w}`),
  'scoreboard players operation @s pmWeapon = @s pmWantW'
 ].join('\n'));
}
