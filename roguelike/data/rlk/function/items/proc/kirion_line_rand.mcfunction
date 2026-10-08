# 무작위 방향 참격 라인 (실행 위치·회전 기준)
execute store result score #kd tmp run random value 1..4
execute if score #kd tmp matches 1 run function rlk:items/proc/kirion_line
execute if score #kd tmp matches 2 run function rlk:items/proc/kirion_line2
execute if score #kd tmp matches 3 run function rlk:items/proc/kirion_line3
execute if score #kd tmp matches 4 run function rlk:items/proc/kirion_line4
