# #peX / #peZ mb = a proposed end point (the player's y): #pOK 1 unless it lies inside a live disc / ring (kind 1-2) or
# line (kind 4) hazard (their own bounds with the body pad).
scoreboard players set #pOK mb 1
execute as @e[type=minecraft:marker,tag=rlk_mb_hz,scores={mbHzK=1..2}] run function rlk:mboss/push/end_disc
execute as @e[type=minecraft:marker,tag=rlk_mb_hz,scores={mbHzK=4}] run function rlk:mboss/push/end_line
