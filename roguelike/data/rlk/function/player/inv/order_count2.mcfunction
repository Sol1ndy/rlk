# macro: ccnt(id), cbase(바닐라 아이템). 임시 점수는 #oc1 · #oc2 (#c2 tmp 는 load 의 상수 2 — char/nefer/cat_tick 이 읽는다)
$execute store result score #oc1 tmp if items entity @s inventory.* $(cbase)[minecraft:custom_data~{rlk:{id:"$(ccnt)"}}]
$execute store result score #oc2 tmp if items entity @s hotbar.* $(cbase)[minecraft:custom_data~{rlk:{id:"$(ccnt)"}}]
scoreboard players operation #oc1 tmp += #oc2 tmp
$execute store result storage rlk:pinv pcnt.$(ccnt) int 1 run scoreboard players get #oc1 tmp
