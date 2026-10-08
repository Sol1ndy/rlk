# macro: ccnt(id), cbase(바닐라 아이템)
$execute store result score #c1 tmp if items entity @s inventory.* $(cbase)[minecraft:custom_data~{rlk:{id:"$(ccnt)"}}]
$execute store result score #c2 tmp if items entity @s hotbar.* $(cbase)[minecraft:custom_data~{rlk:{id:"$(ccnt)"}}]
scoreboard players operation #c1 tmp += #c2 tmp
$execute store result storage rlk:pinv pcnt.$(ccnt) int 1 run scoreboard players get #c1 tmp
