# 주머니 한 틱 (@s = 주머니 허스크, at @s; cm/c3/clean 에서): 모습 유지 · 맥박 · 터짐 / 시듦
scoreboard players operation #pid tmp = @s cmId
execute as @e[tag=rlk_fp_pt,distance=..2] if score @s cmId = #pid tmp run tag @s add rlk_c3this
tag @e[tag=rlk_c3this] add rlk_cmsync
tag @s add rlk_cmsync
execute if entity @s[tag=rlk_c3pop] run return run function rlk:cm/fp/burst
scoreboard players remove @s c3L 1
execute if score @s c3L matches ..0 run return run function rlk:cm/fp/wither
scoreboard players operation #c3m tmp = @s c3L
scoreboard players operation #c3m tmp %= #c3c10 tmp
execute if score @s c3L matches 21.. if score #c3m tmp matches 0 as @e[tag=rlk_c3this] run function rlk:cm/fp/pose/1
execute if score @s c3L matches 21.. if score #c3m tmp matches 5 as @e[tag=rlk_c3this] run function rlk:cm/fp/pose/2
scoreboard players operation #c3m tmp = @s c3L
scoreboard players operation #c3m tmp %= #c3c6 tmp
execute if score @s c3L matches ..20 if score #c3m tmp matches 0 as @e[tag=rlk_c3this] run function rlk:cm/fp/pose/3
execute if score @s c3L matches ..20 if score #c3m tmp matches 3 as @e[tag=rlk_c3this] run function rlk:cm/fp/pose/4
execute if score #c3m tmp matches 1 run particle minecraft:spore_blossom_air ~ ~0.6 ~ 0.25 0.25 0.25 0 2 normal
execute if score @s c3L matches ..20 if score #c3m tmp matches 0 run particle minecraft:happy_villager ~ ~0.5 ~ 0.25 0.2 0.25 0 2 normal
tag @e[tag=rlk_c3this] remove rlk_c3this
