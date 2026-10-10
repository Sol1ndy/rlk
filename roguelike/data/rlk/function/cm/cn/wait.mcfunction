# 조준한 채 대기(대포 방향 고정, 경직 면역)
scoreboard players set #hold tmp 1
scoreboard players remove @s cmT 1
execute as @e[tag=rlk_cmcbw,distance=..6] if score @s cmId = #cid tmp at @s run particle minecraft:smoke ~ ~ ~ 0.05 0.05 0.05 0.01 1
execute if score @s cmT matches ..0 run function rlk:cm/cn/launch
