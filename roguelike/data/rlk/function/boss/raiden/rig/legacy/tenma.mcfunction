# TEMPORARY: rdAnim -> tenma clip.
execute if score @s rdAnim matches 0 run return run function rlk:boss/raiden/rig/play/t_idle
execute if score @s rdAnim matches 1 run return run function rlk:boss/raiden/rig/play/t_idle
execute if score @s rdAnim matches 2 run return run function rlk:boss/raiden/rig/play/t_iai
execute if score @s rdAnim matches 3 run return run execute unless score @s rdRigC matches 33 run function rlk:boss/raiden/rig/play/t_iai
execute if score @s rdAnim matches 4 run return run function rlk:boss/raiden/rig/play/t_combo3
execute if score @s rdAnim matches 5 run return run function rlk:boss/raiden/rig/play/t_rush
execute if score @s rdAnim matches 6 run return run execute unless score @s rdRigC matches 41 run function rlk:boss/raiden/rig/play/t_rush
execute if score @s rdAnim matches 7 run return run function rlk:boss/raiden/rig/play/t_summon
execute if score @s rdAnim matches 8 run return run execute unless score @s rdRigC matches 36 run function rlk:boss/raiden/rig/play/t_summon
execute if score @s rdAnim matches 9 run return run function rlk:boss/raiden/rig/play/transform
execute if score @s rdAnim matches 10 run return run function rlk:boss/raiden/rig/play/t_combo3
execute if score @s rdAnim matches 11 run return run execute unless score @s rdRigC matches 31 run function rlk:boss/raiden/rig/play/t_combo3
execute if score @s rdAnim matches 12 run return run function rlk:boss/raiden/rig/play/t_summon
execute if score @s rdAnim matches 13 run return run execute unless score @s rdRigC matches 36 run function rlk:boss/raiden/rig/play/t_summon
execute if score @s rdAnim matches 14 run return run function rlk:boss/raiden/rig/play/t_seed
execute if score @s rdAnim matches 15 run return run execute unless score @s rdRigC matches 37 run function rlk:boss/raiden/rig/play/t_seed
execute if score @s rdAnim matches 16 run return run function rlk:boss/raiden/rig/play/t_vanish
execute if score @s rdAnim matches 17 run return run execute unless score @s rdRigC matches 39 run function rlk:boss/raiden/rig/play/t_vanish
execute if score @s rdAnim matches 18 run return run function rlk:boss/raiden/rig/play/stagger
execute if score @s rdAnim matches 19 run return run function rlk:boss/raiden/rig/play/death
execute if score @s rdAnim matches 20 run return run function rlk:boss/raiden/rig/play/t_spin_throw
execute if score @s rdAnim matches 21 run return run function rlk:boss/raiden/rig/play/t_rush
execute if score @s rdAnim matches 22 run return run function rlk:boss/raiden/rig/play/exhausted
execute if score @s rdAnim matches 23 run return run function rlk:boss/raiden/rig/play/t_collapse
execute if score @s rdAnim matches 24 run return run function rlk:boss/raiden/rig/play/recover
