# @s = 문. 상태대로 블록을 놓는다. 전투 중인 구역의 문 중 이미 열린 문(지나온 통로)만 철창으로 잠김. 아직 안 가 본 쪽 문은 검은 콘크리트 그대로(건너편이 보이지 않게)
execute if score @s dst matches ..0 run return 0
# 지어지기만 하고 아직 들어가 보지 않은 구역의 다른 통로는 그리지 않는다(그냥 벽으로 보임)
execute if score @s dst matches 1 unless score @s dvis matches 1 run return 0
scoreboard players set #lk tmp 0
execute if score #combat room matches 1.. if score @s da = #combat room run scoreboard players set #lk tmp 1
execute if score #combat room matches 1.. if score @s db = #combat room run scoreboard players set #lk tmp 1
execute if score #lk tmp matches 1 if score @s dst matches 2 run return run function rlk:room/door_bars with entity @s data
execute if score @s dst matches 1 run function rlk:room/door_black with entity @s data
execute if score @s dst matches 2 run function rlk:room/door_air with entity @s data
