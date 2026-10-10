# @s=real living boss; the invisible body owns damage, the displays own appearance.
execute if score @s rdDeath matches 1 run return run function rlk:boss/raiden/death/tick
data merge entity @s {Motion:[0d,0d,0d],Fire:-1s}
execute if score @s rdHitCD matches 1.. run scoreboard players remove @s rdHitCD 1
execute if score @s rdCool matches 1.. run scoreboard players remove @s rdCool 1
scoreboard players add @s rdTime 1
execute if score @s rdPhase matches 0 run scoreboard players add @s rdRage 1
execute if score @s rdPhase matches 0 if score @s rdRage matches 600.. run function rlk:boss/raiden/transform_start
execute if score @s rdPhase matches 1 run function rlk:boss/raiden/transform_tick
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/armor_tick
execute if score @s rdPhase matches 3 run function rlk:boss/raiden/exhausted_tick
execute if score @s rdPhase matches 0 if score @s rdPat matches 0 run function rlk:boss/raiden/idle
execute if score @s rdPhase matches 2 if score @s rdPat matches 0 run function rlk:boss/raiden/idle
execute if score @s rdPat matches 1..6 run function rlk:boss/raiden/normal_dispatch
execute if score @s rdPat matches 11..18 run function rlk:boss/raiden/armor_dispatch
execute if score @s rdPat matches 99 if score @s rdTime matches 60.. run function rlk:boss/raiden/finish
# Keep the body on the disc; all tracking uses the avatar, never the remote camera.
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..21] run tp @s ~ ~ ~
execute if score @s rdBlink matches 1.. run function rlk:boss/raiden/movement/blink_tick
execute unless score @s rdPat matches 5 unless score @s rdPat matches 15 unless score @s rdBlink matches 1.. at @s run function rlk:boss/raiden/rig/tick
# Hide the physical rig while illusions, scattering, or the aerial-arm ultimate are active.
execute if score @s rdPat matches 5 run tp @e[tag=rlk_raiden_part] ~ ~-60 ~
execute if score @s rdPat matches 15 run tp @e[tag=rlk_raiden_part] ~ ~-60 ~
execute if score @s rdBlink matches 1.. run tp @e[tag=rlk_raiden_part] ~ ~-60 ~
execute if score @s rdPat matches 15 run function rlk:boss/raiden/judgment_rig/tick
execute if score @s rdPat matches 15 if score @s rdTime matches 80..173 run function rlk:boss/raiden/camera/try_start
execute if score @s rdPat matches 15 if score @s rdTime matches 174 run function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/bars
