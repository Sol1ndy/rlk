# Video-authored Skirk VFX. @s = player; position = actual body; rotation = locked clip heading.
# pmTick is the animation timeline, 20 ticks per reference second.
execute if score @s pmTick matches 0 run function rlk:char/motion/skirk_fx/skill_right_end/t000
execute if score @s pmTick matches 1 run function rlk:char/motion/skirk_fx/skill_right_end/t001
execute if score @s pmTick matches 2 run function rlk:char/motion/skirk_fx/skill_right_end/t002
execute if score @s pmTick matches 3 run function rlk:char/motion/skirk_fx/skill_right_end/t003
execute if score @s pmTick matches 4 run function rlk:char/motion/skirk_fx/skill_right_end/t004
execute if score @s pmTick matches 5 run function rlk:char/motion/skirk_fx/skill_right_end/t005
execute if score @s pmTick matches 6 run function rlk:char/motion/skirk_fx/skill_right_end/t006
execute if score @s pmTick matches 7 run function rlk:char/motion/skirk_fx/skill_right_end/t007
