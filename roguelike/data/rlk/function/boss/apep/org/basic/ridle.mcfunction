# Lying, without a slot: a slot is asked for every 10 t (the first shot 20 t after it).
execute if score @s apT matches ..9 run return 0
scoreboard players set @s apT 0
execute store result score #apX mb if entity @e[type=minecraft:husk,tag=rlk_mb_ap_tok]
execute if score #apX mb matches 3.. run return 0
tag @s add rlk_mb_ap_tok
scoreboard players set @s apS 7
scoreboard players set @s apT 30
