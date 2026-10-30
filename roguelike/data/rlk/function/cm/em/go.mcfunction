# 돌진: 이 순간 몸이 있는 쪽으로 방향 고정, 거리만큼(4 / 6 / 8틱 × 0.6칸) → 둘이 가운데로 모임. 돌진 중에는 경직 면역
execute facing entity @e[tag=rlk_body,limit=1] feet run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0
execute store result score @s cmYaw run data get entity @e[tag=rlk_cmrot,limit=1] Rotation[0] 100
scoreboard players set @s cmS 2
scoreboard players set @s cmT 8
execute if entity @e[tag=rlk_body,distance=..4.5] run scoreboard players set @s cmT 6
execute if entity @e[tag=rlk_body,distance=..3] run scoreboard players set @s cmT 4
scoreboard players set @s c2T2 0
tag @s add rlk_cmch
execute unless score #c3emdash snd matches 1 run function rlk:cm/c3/snd/emdash
