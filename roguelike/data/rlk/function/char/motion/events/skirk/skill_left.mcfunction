function rlk:char/motion/audio/skirk/skill_left
execute if score @s pmTick matches 0 run scoreboard players set @s pmLockUntil 14
execute if score @s pmTick matches 0 run function rlk:char/motion/control/lock
execute if score @s pmTick matches 9 run function rlk:char/skirk/mode_activate
