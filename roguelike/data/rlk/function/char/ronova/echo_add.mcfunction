# 잔향 +1 (@s = 플레이어, #rvE = 원소 1~8, 9 = 만개 잔향). 얻은 뒤 #rnEcdT 틱 동안은 더 얻지 못함. 3칸이 차 있으면 버린다
execute if score @s rnEcd matches 1.. run return 0
execute if score @s rnE3 matches 1.. run return 0
scoreboard players operation @s rnEcd = #rnEcdT tmp
function rlk:char/ronova/echo_push
