execute at @s run tp @s ^ ^ ^0.85
execute at @s unless block ~ ~ ~ #minecraft:replaceable run return run function rlk:char/lumine/jav_break
# 판정은 여유롭게: 투창 주변 ±1칸 상자에 몸이 걸친 적
execute at @s positioned ~-1 ~-1 ~-1 if entity @e[tag=rlk_mob,dx=1,dy=1,dz=1] run function rlk:char/lumine/jav_hit
