function rlk:char/motion/audio/arle/skill
execute if score @s pmTick matches 0 run scoreboard players set @s pmLockUntil 21
execute if score @s pmTick matches 0 run function rlk:char/motion/control/lock
execute if score @s pmTick matches 7 if entity @e[tag=rlk_artg,limit=1] run function rlk:char/arlecchino/skill_dash
execute if score @s pmTick matches 14 at @e[tag=rlk_body,limit=1] run function rlk:char/arlecchino/skill_go
