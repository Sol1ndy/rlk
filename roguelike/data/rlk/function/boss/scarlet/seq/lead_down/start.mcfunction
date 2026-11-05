# lead_down (PLAN §3.5): the kip-up, the hat, the side steps, the shield refill, the hat on, the glow, the darkness + the brim (A13 at its end).
# Start (@s = the body, at it; #sq hr = 0).
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_stage"]}
execute as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] at @s rotated as @e[tag=rlk_body,limit=1] run tp @s ~ ~ ~ ~ 0
function rlk:boss/scarlet/rig/play/lead_down
scoreboard players set #sqdone hr 0
