# 재연 (@s = 플레이어, at 몸): 가장 오래된 잔향을 그 원소의 탄으로 다시 쏜다. 만개 잔향이면 다음 잔향도 함께(두 발)
execute if score @s rnFcd matches 1.. run return 0
execute unless score @s rnE1 matches 1.. run return run function rlk:char/deny {t:"잔향이 없음"}
scoreboard players operation #rvE tmp = @s rnE1
function rlk:char/ronova/shift
scoreboard players operation @s rnFcd = #rnGap tmp
scoreboard players set #pOff tmp 0
execute if score #rvE tmp matches 9 if score @s rnE1 matches 1.. run scoreboard players set #pOff tmp 1
execute rotated as @s run function rlk:char/ronova/echo_fire
execute if score #pOff tmp matches 1 rotated as @s run function rlk:char/ronova/bloom_pair
scoreboard players set #pOff tmp 0
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
