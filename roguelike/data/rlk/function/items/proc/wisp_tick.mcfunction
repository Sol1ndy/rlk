# @s = 바람뭉치, at @s. 시간이 다 되면 반경 3.5칸에 공격력의 70퍼센트 얼음 원소 피해
scoreboard players remove @s life 1
particle minecraft:snowflake ~ ~ ~ 0.25 0.25 0.25 0.02 2
particle minecraft:end_rod ~ ~ ~ 0.2 0.2 0.2 0.01 1
execute if score @s life matches 1.. run return 0
particle minecraft:snowflake ~ ~ ~ 1.6 0.6 1.6 0.12 60
particle minecraft:end_rod ~ ~ ~ 1.2 0.5 1.2 0.08 20
playsound minecraft:block.glass.break master @a ~ ~ ~ 0.7 1.5
playsound minecraft:entity.breeze.wind_burst master @a ~ ~ ~ 0.5 1.4
execute positioned ~ ~-1 ~ run function rlk:items/proc/wisp_boom
kill @s
