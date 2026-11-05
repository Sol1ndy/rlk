# CS4 ending (PLAN §3.7 std): the ground slash, the duel, the aerial exchange, the landing, the walk-in and sheathe, lines 17-23, the hat-tip; H at its end.
# Start (@s = the body, at it; #sq hr = 0).
function rlk:boss/scarlet/rig/face/player
execute as @a[tag=player,limit=1] anchored eyes run rotate @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] eyes
rotate @e[tag=rlk_av,limit=1] facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_stage"]}
execute as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rlk:boss/scarlet/rig/play/ending
scoreboard players set #sqdone hr 0
scoreboard players set @a[tag=player] hudHold 2
title @a[tag=player] actionbar ""
