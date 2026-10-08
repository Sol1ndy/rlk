# 파편 명중 (@s = 파편): 잠식 +5% → 얼음 피해(반응 피해, 부착 없음)
scoreboard players operation #shD tmp = @s rxDmg
execute at @s run particle minecraft:block{block_state:"minecraft:packed_ice"} ~ ~ ~ 0.15 0.15 0.15 0.1 10
execute at @s run playsound minecraft:block.glass.hit master @a ~ ~ ~ 0.6 1.6
kill @s
scoreboard players set #g tmp 5
execute as @e[tag=rlk_rntgt] run function rlk:element/void/er_add
scoreboard players operation #dmg tmp = #shD tmp
scoreboard players set #elem tmp 4
execute as @e[tag=rlk_rntgt] at @s run function rlk:element/dot
