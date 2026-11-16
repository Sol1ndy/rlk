# The growing ribbon (blade.py; rlk_hr_trg: one at a time; @s = the body, at the hand's place now): it turns to the
# marker rlk_hr_trt (the hand's place one tick ago) and becomes as long as the way to it (one tick of interpolation: one
# step behind her model, never ahead of it), then the marker comes here.
execute as @e[type=minecraft:item_display,tag=rlk_hr_trg] at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_trt,limit=1] feet run function rlk:boss/scarlet/core/sw/rib1
tp @e[type=minecraft:marker,tag=rlk_hr_trt,limit=1] ~ ~ ~
