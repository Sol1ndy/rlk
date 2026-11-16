# 물줄기 한 칸(0.5칸씩 술사 쪽으로, 최대 16칸 = 8칸 거리): 물빛 입자 + 물방울. 술사 1칸 안에서 멈춤
particle minecraft:dust{color:[0.3,0.7,1.0],scale:1.0} ~ ~ ~ 0.03 0.03 0.03 0 2 normal
particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0 1 normal
scoreboard players remove #c3rs tmp 1
execute if score #c3rs tmp matches ..0 run return 0
execute if entity @e[tag=rlk_c3heal,distance=..1.6] run return 0
execute positioned ^ ^ ^0.5 run function rlk:cm/cw/ribbon
