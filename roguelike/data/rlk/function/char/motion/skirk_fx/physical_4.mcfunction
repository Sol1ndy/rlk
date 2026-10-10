# Video-authored Skirk VFX. @s = player; position = actual body; rotation = locked clip heading.
# pmTick is the animation timeline, 20 ticks per reference second.
execute if score @s pmTick matches 4 run function rlk:char/motion/skirk_fx/physical_4/t004
execute if score @s pmTick matches 5 run function rlk:char/motion/skirk_fx/physical_4/t005
execute if score @s pmTick matches 6 run function rlk:char/motion/skirk_fx/physical_4/t006
