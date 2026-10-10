# 던질 투창이 남아 있음 (@s = 플레이어, at @s): 3틱마다 하나씩, 그 순간 바라보는 방향으로
scoreboard players remove @s javT 1
execute if score @s javT matches 1.. run return 0
scoreboard players set @s javT 3
scoreboard players operation #ji tmp = @s javN
scoreboard players operation #ji tmp -= @s javQ
scoreboard players remove @s javQ 1
# 조준점 = 시선 방향 16칸 앞. 투창은 눈 옆에서 생겨 조준점을 향함
execute positioned ~ ~1.62 ~ positioned ^ ^ ^16 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_aimpt"]}
execute if score #ji tmp matches 0 positioned ~ ~1.62 ~ positioned ^ ^0.35 ^0.8 run function rlk:char/lumine/jav_spawn
execute if score #ji tmp matches 1 positioned ~ ~1.62 ~ positioned ^0.8 ^0.15 ^0.6 run function rlk:char/lumine/jav_spawn
execute if score #ji tmp matches 2 positioned ~ ~1.62 ~ positioned ^-0.8 ^0.15 ^0.6 run function rlk:char/lumine/jav_spawn
execute if score #ji tmp matches 3 positioned ~ ~1.62 ~ positioned ^1.4 ^0.5 ^0.4 run function rlk:char/lumine/jav_spawn
execute if score #ji tmp matches 4.. positioned ~ ~1.62 ~ positioned ^-1.4 ^0.5 ^0.4 run function rlk:char/lumine/jav_spawn
kill @e[tag=rlk_aimpt]
