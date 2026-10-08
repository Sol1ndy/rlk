# 바닥 한가운데 무늬 = 구역 종류, 지도에서도 구분됨 (@s = 구역 표식, at @s)
fill ~-5 ~ ~-5 ~4 ~ ~4 minecraft:air replace #rlk:plants
execute if score @s zkind matches 2 run fill ~-3 ~-1 ~-3 ~2 ~-1 ~2 minecraft:quartz_block
execute if score @s zkind matches 3 run fill ~-3 ~-1 ~-3 ~2 ~-1 ~2 minecraft:yellow_concrete
execute if score @s zkind matches 4 run fill ~-3 ~-1 ~-3 ~2 ~-1 ~2 minecraft:orange_concrete
execute if score @s zkind matches 5 run fill ~-3 ~-1 ~-3 ~2 ~-1 ~2 minecraft:light_blue_concrete
execute if score @s zkind matches 6 run fill ~-3 ~-1 ~-3 ~2 ~-1 ~2 minecraft:red_concrete
execute if score @s zkind matches 7 run fill ~-3 ~-1 ~-3 ~2 ~-1 ~2 minecraft:purple_concrete
execute if score @s zkind matches 8 run fill ~-3 ~-1 ~-3 ~2 ~-1 ~2 minecraft:moss_block
execute if score @s zkind matches 9 run fill ~-5 ~-1 ~-5 ~4 ~-1 ~4 minecraft:polished_granite
execute if score @s zkind matches 10 run fill ~-3 ~-1 ~-3 ~2 ~-1 ~2 minecraft:lime_concrete
