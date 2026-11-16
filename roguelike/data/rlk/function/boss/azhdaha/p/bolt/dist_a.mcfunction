# Inside a safe circle at the player's feet (R0 3.2 + 0.3): #aq42D 0, else 1.
scoreboard players set #aq42D mb 1
execute at @e[tag=rlk_body,limit=1] if entity @e[type=minecraft:marker,tag=rlk_mb_az_p42s,distance=..3.5] run scoreboard players set #aq42D mb 0
