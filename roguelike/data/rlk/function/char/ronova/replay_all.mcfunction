# 신벌 마무리: 잔향 전부를 소모하지 않고 한 번에 재연(왼쪽 · 가운데 · 오른쪽)
scoreboard players set #pOff tmp 0
execute if score @s rnE1 matches 1.. run scoreboard players operation #rvE tmp = @s rnE1
execute if score @s rnE1 matches 1.. rotated ~-14 ~ run function rlk:char/ronova/echo_fire
execute if score @s rnE2 matches 1.. run scoreboard players operation #rvE tmp = @s rnE2
execute if score @s rnE2 matches 1.. run function rlk:char/ronova/echo_fire
execute if score @s rnE3 matches 1.. run scoreboard players operation #rvE tmp = @s rnE3
execute if score @s rnE3 matches 1.. rotated ~14 ~ run function rlk:char/ronova/echo_fire
