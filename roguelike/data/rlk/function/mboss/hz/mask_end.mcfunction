# @s = an expiring mask hazard with its own safe group (made with #hzSafeG 0): its safe markers go with it.
scoreboard players operation #hzG2 mb = @s mbHzSG
execute as @e[type=minecraft:marker,tag=rlk_mb_hzsafe] if score @s mbHzSG = #hzG2 mb run kill @s
