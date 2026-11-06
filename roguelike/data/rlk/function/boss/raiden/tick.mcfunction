# @s=real living boss; the invisible body owns damage, the displays own appearance.
execute if score @s rdDeath matches 1 run return run function rlk:boss/raiden/death/tick
data merge entity @s {Motion:[0d,0d,0d],Fire:-1s}
execute if score @s rdHitCD matches 1.. run scoreboard players remove @s rdHitCD 1
execute if score @s rdCool matches 1.. run scoreboard players remove @s rdCool 1
scoreboard players add @s rdTime 1
execute if score @s rdPhase matches 0 run scoreboard players add @s rdRage 1
# A full gauge waits for the running pattern (and any blink) to finish, then the boss transforms where she stands.
# The forced follow-ups (몽상의 일심 after 찰나의 포영, the multi eye after the single eye) come first.
execute if score @s rdPhase matches 0 if score @s rdRage matches 900.. if score @s rdPat matches 0 unless score @s rdBlink matches 1.. unless score @s rdNext matches 7 unless score @s rdSgEye matches 1.. run function rlk:boss/raiden/transform_start
execute if score @s rdPhase matches 1 run function rlk:boss/raiden/transform_tick
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/armor_tick
execute if score @s rdPhase matches 3 run function rlk:boss/raiden/exhausted_tick
execute if score @s rdPhase matches 0 if score @s rdPat matches 0 run function rlk:boss/raiden/idle
execute if score @s rdPhase matches 2 if score @s rdPat matches 0 run function rlk:boss/raiden/idle
# A pattern that must close in first blinks (rdGo); its clock waits at 0 meanwhile.
execute if score @s rdGo matches 1.. if score @s rdPat matches 1..28 run function rlk:boss/raiden/close_in
# Phase-0 timelines run from rdTime 0 (the choose tick); phase-2 timelines from rdTime 1 (as in the release).
execute if score @s rdGo matches 0 if score @s rdPat matches 1..10 run function rlk:boss/raiden/normal_dispatch
execute if score @s rdGo matches 0 if score @s rdPat matches 21..28 run function rlk:boss/raiden/normal_dispatch
execute if score @s rdGo matches 0 if score @s rdPat matches 11..20 if score @s rdTime matches 1.. run function rlk:boss/raiden/armor_dispatch
execute if score @s rdPat matches 99 if score @s rdTime matches 60.. run function rlk:boss/raiden/finish
# Stuns (rdPat 98: real clone found, single eye broken, guard broken), shogun.py.
execute if score @s rdPat matches 98 run function rlk:boss/raiden/sg/stun_tick
# Keep the body on the disc without snapping: slide back toward the centre, and only
# blink home if it is somehow far outside. Tracking uses the avatar, never the camera.
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..21] at @s facing entity @e[tag=rlk_raiden_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.45 run tp @s ~ ~ ~
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..26] unless score @s rdBlink matches 1.. run function rlk:boss/raiden/movement/blink_to
execute if score @s rdBlink matches 1.. run function rlk:boss/raiden/movement/blink_tick
# Phase-0 per-tick state (rear-hit memory, counter cooldown, the switch after-effects); off in every other phase.
execute if score @s rdPhase matches 0 run function rlk:boss/raiden/sg/tick
execute unless score @s rdPhase matches 0 if score @s rdSgFx matches 1.. run function rlk:boss/raiden/sg/fx_off
# Rig visibility: #rdHide 1 hides every part (rig/state/hidden, scale 0 where they stand; never moved) on the
# first hidden tick; the first visible tick queues the form's idle clip unless a clip is already queued.
scoreboard players set #rdHide rd 0
execute if score @s rdPat matches 5 if score #rdIlStep rd matches 1..2 run scoreboard players set #rdHide rd 1
execute if score #rdHide rd matches 1 unless score @s rdHidden matches 1 run function rlk:boss/raiden/sg/rig_hide
execute if score #rdHide rd matches 0 if score @s rdHidden matches 1.. run function rlk:boss/raiden/sg/rig_show
execute if score #rdHide rd matches 0 at @s run function rlk:boss/raiden/rig/tick
execute if score #rdHide rd matches 1 at @s rotated as @s rotated ~ 0 run function rlk:boss/raiden/rig/follow

function rlk:boss/raiden/bars
