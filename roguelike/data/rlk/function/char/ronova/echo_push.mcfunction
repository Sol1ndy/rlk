# 잔향 +1, 대기 없이 (@s = 플레이어, #rvE = 원소 1~8, 9 = 만개 잔향). 3칸이 차 있으면 버린다
execute if score @s rnE3 matches 1.. run return 0
execute unless score #k42 snd matches 1 run function rlk:snd/f295
execute unless score @s rnE1 matches 1.. run return run scoreboard players operation @s rnE1 = #rvE tmp
execute unless score @s rnE2 matches 1.. run return run scoreboard players operation @s rnE2 = #rvE tmp
scoreboard players operation @s rnE3 = #rvE tmp
