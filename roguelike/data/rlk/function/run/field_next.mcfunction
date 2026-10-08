# 다음 맵으로 넘어가기 직전 (run/next_map): 떨어진 아이템은 팔고, 골드·사파이어 조각은 줍고, 나머지는 지운다
scoreboard players operation #fg0 tmp = @a[tag=player,limit=1] gold
execute store result score #fn tmp if entity @e[tag=rlk_ditem]
execute as @e[tag=rlk_ditem] at @s run function rlk:ditem/do_sell
scoreboard players operation #fg1 tmp = @a[tag=player,limit=1] gold
scoreboard players operation #fg1 tmp -= #fg0 tmp
execute if score #fn tmp matches 1.. run tellraw @a[tag=player] [{"text":"[런] ","color":"gold","bold":true},{"text":"바닥에 두고 온 아이템 ","color":"gray","bold":false},{"score":{"name":"#fn","objective":"tmp"},"color":"white","bold":false},{"text":"개를 팔았습니다. ","color":"gray","bold":false},{"text":"◆ +","color":"#E0B255","bold":false},{"score":{"name":"#fg1","objective":"tmp"},"color":"#E0B255","bold":false}]
execute as @e[tag=rlk_gold] run function rlk:combat/gold_absorb
function rlk:run/field_clear
