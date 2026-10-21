# Hail ambience over every live 45 hail field (the field pool card is the floor read); the chain ends
# with the last field.
scoreboard players set #aq45H mb 0
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p45h] at @s run function rlk:mboss/azhdaha/fx/p/hail {r:40}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p45h,limit=1] run function rlk:mboss/azhdaha/fx/snd/hail
execute if entity @e[type=minecraft:marker,tag=rlk_mb_az_p45h,limit=1] run scoreboard players set #aq45H mb 1
execute if score #aq45H mb matches 1 run scoreboard players set #azAftF mb 43
execute if score #aq45H mb matches 1 run scoreboard players set #azAftD mb 8
execute if score #aq45H mb matches 1 run function rlk:mboss/azhdaha/aft/new
