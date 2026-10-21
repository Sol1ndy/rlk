# TEMPORARY: rdAnim -> shogun clip.
execute if score @s rdAnim matches 0 run return run function rlk:boss/raiden/rig/legacy/shogun_0
execute if score @s rdAnim matches 1 run return run function rlk:boss/raiden/rig/legacy/shogun_1
execute if score @s rdAnim matches 2 run return run function rlk:boss/raiden/rig/play/iai_near
execute if score @s rdAnim matches 3 run return run execute unless score @s rdRigC matches 5 run function rlk:boss/raiden/rig/play/iai_near
execute if score @s rdAnim matches 4 run return run function rlk:boss/raiden/rig/play/combo5
execute if score @s rdAnim matches 5 run return run function rlk:boss/raiden/rig/play/p_lance
execute if score @s rdAnim matches 6 run return run execute unless score @s rdRigC matches 18 run function rlk:boss/raiden/rig/play/p_lance
execute if score @s rdAnim matches 7 run return run function rlk:boss/raiden/rig/play/cast
execute if score @s rdAnim matches 8 run return run execute unless score @s rdRigC matches 23 run function rlk:boss/raiden/rig/play/cast
execute if score @s rdAnim matches 9 run return run function rlk:boss/raiden/rig/play/transform
execute if score @s rdAnim matches 10 run return run function rlk:boss/raiden/rig/play/combo5
execute if score @s rdAnim matches 11 run return run execute unless score @s rdRigC matches 6 run function rlk:boss/raiden/rig/play/combo5
execute if score @s rdAnim matches 12 run return run function rlk:boss/raiden/rig/play/cast
execute if score @s rdAnim matches 13 run return run execute unless score @s rdRigC matches 23 run function rlk:boss/raiden/rig/play/cast
execute if score @s rdAnim matches 14 run return run function rlk:boss/raiden/rig/play/cast
execute if score @s rdAnim matches 15 run return run execute unless score @s rdRigC matches 23 run function rlk:boss/raiden/rig/play/cast
execute if score @s rdAnim matches 16 run return run function rlk:boss/raiden/rig/play/cast
execute if score @s rdAnim matches 17 run return run execute unless score @s rdRigC matches 23 run function rlk:boss/raiden/rig/play/cast
execute if score @s rdAnim matches 18 run return run function rlk:boss/raiden/rig/play/stagger
execute if score @s rdAnim matches 19 run return run function rlk:boss/raiden/rig/play/death
execute if score @s rdAnim matches 20 run return run function rlk:boss/raiden/rig/play/p_twirl_slam
execute if score @s rdAnim matches 21 run return run function rlk:boss/raiden/rig/play/iai_dash
execute if score @s rdAnim matches 22 run return run function rlk:boss/raiden/rig/play/exhausted
execute if score @s rdAnim matches 23 run return run function rlk:boss/raiden/rig/play/t_collapse
execute if score @s rdAnim matches 24 run return run function rlk:boss/raiden/rig/play/recover
