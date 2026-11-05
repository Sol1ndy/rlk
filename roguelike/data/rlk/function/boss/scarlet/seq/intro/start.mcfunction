# CS0 intro (PLAN §3.1): seated with the cup and bottle, lines 1-10, the walk, the scabbard raised; intro_end: line 11, the draw, the stance.
# Start (@s = the body, at it; #sq hr = 0).
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_stage"]}
execute as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] at @s rotated as @e[tag=rlk_body,limit=1] run tp @s ~ ~ ~ ~ 0
function rlk:boss/scarlet/rig/play/intro
scoreboard players set #sqdone hr 0
