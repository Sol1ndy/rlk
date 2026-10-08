# 반응한 원소를 로노바의 잔향으로 (@s = 맞은 몹, #rvN = 원소). 재연이 일으킨 반응(#rnNoEcho, 재연에 맞은 지 10초 안 rnNoE)은 남기지 않는다. 풀 → 만개 잔향(9)
execute unless score #charN tmp matches 7 run return 0
execute if score #rnNoEcho tmp matches 1 run return 0
execute if score @s rnNoE matches 1.. run return 0
scoreboard players operation #rvE tmp = #rvN tmp
execute if score #rvE tmp matches 7 run scoreboard players set #rvE tmp 9
execute as @a[tag=player,limit=1] run function rlk:char/ronova/echo_add
