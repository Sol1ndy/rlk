# @s = unique real boss. Parts inherit body yaw but never pitch.
execute unless entity @e[tag=rlk_raiden_part,limit=1] run function rlk:boss/raiden/rig/spawn
execute rotated as @s rotated ~ 0 run tp @e[tag=rlk_raiden_part] ~ ~ ~ ~ 0
execute unless score @s rdAnim = @s rdRigA run function rlk:boss/raiden/rig/changed
execute unless score @s rdPhase = @s rdRigP run function rlk:boss/raiden/rig/changed
execute if score @s rdAnim matches 0 run function rlk:boss/raiden/rig/clip/idle
execute if score @s rdAnim matches 1 run function rlk:boss/raiden/rig/clip/walk
execute if score @s rdAnim matches 2 run function rlk:boss/raiden/rig/clip/slash_wind
execute if score @s rdAnim matches 3 run function rlk:boss/raiden/rig/clip/slash_a
execute if score @s rdAnim matches 4 run function rlk:boss/raiden/rig/clip/slash_b
execute if score @s rdAnim matches 5 run function rlk:boss/raiden/rig/clip/thrust_wind
execute if score @s rdAnim matches 6 run function rlk:boss/raiden/rig/clip/thrust
execute if score @s rdAnim matches 7 run function rlk:boss/raiden/rig/clip/cast_wind
execute if score @s rdAnim matches 8 run function rlk:boss/raiden/rig/clip/cast
execute if score @s rdAnim matches 9 run function rlk:boss/raiden/rig/clip/transform
execute if score @s rdAnim matches 10 run function rlk:boss/raiden/rig/clip/arm_sweep_wind
execute if score @s rdAnim matches 11 run function rlk:boss/raiden/rig/clip/arm_sweep
execute if score @s rdAnim matches 12 run function rlk:boss/raiden/rig/clip/clap_wind
execute if score @s rdAnim matches 13 run function rlk:boss/raiden/rig/clip/clap
execute if score @s rdAnim matches 14 run function rlk:boss/raiden/rig/clip/slam_wind
execute if score @s rdAnim matches 15 run function rlk:boss/raiden/rig/clip/slam
execute if score @s rdAnim matches 16 run function rlk:boss/raiden/rig/clip/judgment_wind
execute if score @s rdAnim matches 17 run function rlk:boss/raiden/rig/clip/judgment
execute if score @s rdAnim matches 18 run function rlk:boss/raiden/rig/clip/stagger
execute if score @s rdAnim matches 19 run function rlk:boss/raiden/rig/clip/death
execute if score @s rdAnim matches 20 run function rlk:boss/raiden/rig/clip/spin
execute if score @s rdAnim matches 21 run function rlk:boss/raiden/rig/clip/dash
execute if score @s rdAnim matches 22 run function rlk:boss/raiden/rig/clip/exhausted
execute if score @s rdAnim matches 23 run function rlk:boss/raiden/rig/clip/collapse
execute if score @s rdAnim matches 24 run function rlk:boss/raiden/rig/clip/recover
function rlk:boss/raiden/rig/lightning_tick
execute if score @s rdRigHit matches 1 run execute as @e[tag=rlk_raiden_part] run data merge entity @s {Glowing:0b}
execute if score @s rdRigHit matches 1.. run scoreboard players remove @s rdRigHit 1
scoreboard players add @s rdRigT 1
