# Fronts and the walk go (selectors only).
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/mv/stop
scoreboard players set #mbNoLeash mb 0
kill @e[type=minecraft:marker,tag=rlk_mb_az_p20w1]
kill @e[type=minecraft:marker,tag=rlk_mb_az_p20w2]
kill @e[type=minecraft:marker,tag=rlk_mb_az_p20w3]
kill @e[type=minecraft:marker,tag=rlk_mb_az_p20w4]
kill @e[type=minecraft:marker,tag=rlk_mb_az_p20w5]
kill @e[type=minecraft:marker,tag=rlk_mb_az_p20w6]
