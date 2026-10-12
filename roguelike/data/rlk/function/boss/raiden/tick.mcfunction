# @s=real living boss; the invisible body owns damage, the displays own appearance.
execute if score @s rdDeath matches 1 run return run function rlk:boss/raiden/death/tick
data merge entity @s {Motion:[0d,0d,0d],Fire:-1s}
execute if score @s rdHitCD matches 1.. run scoreboard players remove @s rdHitCD 1
execute if score @s rdCool matches 1.. run scoreboard players remove @s rdCool 1
scoreboard players add @s rdTime 1
execute if score @s rdPhase matches 0 run scoreboard players add @s rdRage 1
# A full gauge waits for the running pattern (and any blink) to finish, then the
# boss transforms where it stands.
execute if score @s rdPhase matches 0 if score @s rdRage matches 900.. if score @s rdPat matches 0 unless score @s rdBlink matches 1.. run function rlk:boss/raiden/transform_start
execute if score @s rdPhase matches 1 run function rlk:boss/raiden/transform_tick
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/armor_tick
execute if score @s rdPhase matches 3 run function rlk:boss/raiden/exhausted_tick
execute if score @s rdPhase matches 0 if score @s rdPat matches 0 run function rlk:boss/raiden/idle
execute if score @s rdPhase matches 2 if score @s rdPat matches 0 run function rlk:boss/raiden/idle
# Timelines start on the tick after choose: rdTime 1 is every pattern's first frame.
execute if score @s rdPat matches 1..7 if score @s rdTime matches 1.. run function rlk:boss/raiden/normal_dispatch
execute if score @s rdPat matches 11..18 if score @s rdTime matches 1.. run function rlk:boss/raiden/armor_dispatch
execute if score @s rdPat matches 99 if score @s rdTime matches 60.. run function rlk:boss/raiden/finish
# Found the real illusion: a 10 s stun owned by the illusion generator.
execute if score @s rdPat matches 98 run function rlk:boss/raiden/illusion/stun_tick
# Keep the body on the disc without snapping: slide back toward the centre, and only
# scatter-blink home if it is somehow far outside. Tracking uses the avatar, never the camera.
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..21] at @s facing entity @e[tag=rlk_raiden_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.45 run tp @s ~ ~ ~
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..26] unless score @s rdBlink matches 1.. run function rlk:boss/raiden/movement/blink_to
execute if score @s rdBlink matches 1.. run function rlk:boss/raiden/movement/blink_tick
# Hide the physical rig while illusions, scattering, or the aerial-arm ultimate are active.
scoreboard players set #rdHide rd 0
execute if score @s rdBlink matches 1.. run scoreboard players set #rdHide rd 1
execute if score @s rdPat matches 5 if score @s rdTime matches 1.. run scoreboard players set #rdHide rd 1
execute if score @s rdPat matches 15 if score @s rdTime matches 26.. run scoreboard players set #rdHide rd 1
execute if score #rdHide rd matches 0 at @s run function rlk:boss/raiden/rig/tick
execute if score #rdHide rd matches 1 run function rlk:boss/raiden/rig_hide
execute if score #rdHide rd matches 0 if score @s rdHidden matches 1.. run function rlk:boss/raiden/rig_shown
execute if score @s rdPat matches 15 run function rlk:boss/raiden/judgment_rig/tick
execute if score @s rdPat matches 15 if score @s rdTime matches 80..173 run function rlk:boss/raiden/camera/try_start
execute if score @s rdPat matches 15 if score @s rdTime matches 174 run function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/bars
