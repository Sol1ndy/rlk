# lead_stand {g:"a8"|"a13"} (PLAN §3.5): the stagger, the hat, the side steps, the refill, the darkness + the brim (the gauntlet g at its end).
# Start (@s = the body, at it; #sq hr = 0) — macro.
scoreboard players set #sq_g hr 0
$data modify storage rlk:hr seq.g set value "$(g)"
execute if data storage rlk:hr seq{g:"a8"} run function rlk:boss/scarlet/seq/lead_stand/g/a8
execute if data storage rlk:hr seq{g:"a13"} run function rlk:boss/scarlet/seq/lead_stand/g/a13
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_stage"]}
execute as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] at @s rotated as @e[tag=rlk_body,limit=1] run tp @s ~ ~ ~ ~ 0
function rlk:boss/scarlet/rig/play/lead_stand
scoreboard players set #sqdone hr 0
