scoreboard players set @s rdRigT 0
scoreboard players operation @s rdRigA = @s rdAnim
scoreboard players operation @s rdRigP = @s rdPhase
execute if score @s rdAnim matches 0 run function rlk:boss/raiden/rig/select/idle
execute if score @s rdAnim matches 1 run function rlk:boss/raiden/rig/select/walk
execute if score @s rdAnim matches 2 run function rlk:boss/raiden/rig/select/slash_wind
execute if score @s rdAnim matches 3 run function rlk:boss/raiden/rig/select/slash_a
execute if score @s rdAnim matches 4 run function rlk:boss/raiden/rig/select/slash_b
execute if score @s rdAnim matches 5 run function rlk:boss/raiden/rig/select/thrust_wind
execute if score @s rdAnim matches 6 run function rlk:boss/raiden/rig/select/thrust
execute if score @s rdAnim matches 7 run function rlk:boss/raiden/rig/select/cast_wind
execute if score @s rdAnim matches 8 run function rlk:boss/raiden/rig/select/cast
execute if score @s rdAnim matches 9 run function rlk:boss/raiden/rig/select/transform
execute if score @s rdAnim matches 10 run function rlk:boss/raiden/rig/select/arm_sweep_wind
execute if score @s rdAnim matches 11 run function rlk:boss/raiden/rig/select/arm_sweep
execute if score @s rdAnim matches 12 run function rlk:boss/raiden/rig/select/clap_wind
execute if score @s rdAnim matches 13 run function rlk:boss/raiden/rig/select/clap
execute if score @s rdAnim matches 14 run function rlk:boss/raiden/rig/select/slam_wind
execute if score @s rdAnim matches 15 run function rlk:boss/raiden/rig/select/slam
execute if score @s rdAnim matches 16 run function rlk:boss/raiden/rig/select/judgment_wind
execute if score @s rdAnim matches 17 run function rlk:boss/raiden/rig/select/judgment
execute if score @s rdAnim matches 18 run function rlk:boss/raiden/rig/select/stagger
execute if score @s rdAnim matches 19 run function rlk:boss/raiden/rig/select/death
execute if score @s rdAnim matches 20 run function rlk:boss/raiden/rig/select/spin
execute if score @s rdAnim matches 21 run function rlk:boss/raiden/rig/select/dash
execute if score @s rdAnim matches 22 run function rlk:boss/raiden/rig/select/exhausted
execute if score @s rdAnim matches 23 run function rlk:boss/raiden/rig/select/collapse
execute if score @s rdAnim matches 24 run function rlk:boss/raiden/rig/select/recover
