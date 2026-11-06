# 달라붙음(예고 1초, 바닥 고리가 따라옴): 경직 · 빙결이면 취소. 마지막 6틱은 고리가 번쩍
scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return run function rlk:cm/cancel
scoreboard players remove @s cmT 1
execute if score #c2X tmp matches 1 run scoreboard players remove @s cmT 1
execute as @e[tag=rlk_c2ring,distance=..4] if score @s cmId = #cid tmp run function rlk:cm/ss/ring_keep
execute if score @s cmT matches 1.. run particle minecraft:electric_spark ~ ~0.3 ~ 0.3 0.2 0.3 0.05 1 normal
execute if score @s cmT matches 6 as @e[tag=rlk_c2ring,distance=..4] if score @s cmId = #cid tmp run data merge entity @s {Glowing:1b,glow_color_override:13404415}
execute if score @s cmT matches ..0 run function rlk:cm/ss/shock
