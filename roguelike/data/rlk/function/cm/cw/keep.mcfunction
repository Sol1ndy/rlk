# 거리 두기: 10칸 안이면 더 다가오지 않고, 7칸 안이면 3틱마다 몸 반대쪽으로(뒤 1.2칸이 지나갈 수 있을 때만)
execute unless entity @e[tag=rlk_body,limit=1] run return 0
execute if entity @e[tag=rlk_body,distance=..10] run scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return 0
execute if score @s c2T matches 1.. run scoreboard players remove @s c2T 1
execute unless entity @e[tag=rlk_body,distance=..7] run return 0
execute if score @s c2T matches 1.. run return 0
scoreboard players set @s c2T 3
scoreboard players set #c2Fw tmp 230
scoreboard players set #c2Up tmp -1
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ^ ^ ^1.2 if function rlk:cm/c3/col_ok positioned ^ ^ ^-1.2 run function rlk:cm/c2/impulse
