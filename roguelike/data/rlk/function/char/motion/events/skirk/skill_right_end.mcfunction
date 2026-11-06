function rlk:char/motion/audio/skirk/skill_right_end
execute if score @s pmTick matches 0 run scoreboard players set @s pmLockUntil 4
execute if score @s pmTick matches 0 run function rlk:char/motion/control/lock
