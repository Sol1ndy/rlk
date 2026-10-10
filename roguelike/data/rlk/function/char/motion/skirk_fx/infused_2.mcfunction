# Video-authored Skirk VFX. @s = player; position = actual body; rotation = locked clip heading.
# pmTick is the animation timeline, 20 ticks per reference second.
execute if score @s pmTick matches 0 run function rlk:char/motion/skirk_fx/infused_2/t000
execute if score @s pmTick matches 2 run function rlk:char/motion/skirk_fx/infused_2/t002
execute if score @s pmTick matches 3 run function rlk:char/motion/skirk_fx/infused_2/t003
execute if score @s pmTick matches 4 run function rlk:char/motion/skirk_fx/infused_2/t004
