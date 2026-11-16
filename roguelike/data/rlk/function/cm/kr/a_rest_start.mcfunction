# spent after the third dash: 24 t standing still, staggerable (the punish window)
scoreboard players set @s cmS 3
scoreboard players set @s cmT 24
tag @s remove rlk_cmch
tag @s remove rlk_c2_fix
scoreboard players set @s cmCd 64
execute if score @s cmCd2 matches ..19 run scoreboard players set @s cmCd2 20
particle minecraft:large_smoke ~ ~1.6 ~ 0.2 0.1 0.2 0.01 4
playsound minecraft:block.fire.extinguish master @a ~ ~ ~ 0.6 1.5
