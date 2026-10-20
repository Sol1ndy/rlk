# Core service 27: a scripted turn step (#azTurnK 1 turn45_l 2 turn45_r 3 turn90_l 4 turn90_r 5 turn180
# 6 turn180 mirrored), the yaw driver turns the anchor by the manifest schedule.
execute if score #azTurnK mb matches 1 run return run function rlk:mboss/azhdaha/yaw/play_turn45_l
execute if score #azTurnK mb matches 2 run return run function rlk:mboss/azhdaha/yaw/play_turn45_r
execute if score #azTurnK mb matches 3 run return run function rlk:mboss/azhdaha/yaw/play_turn90_l
execute if score #azTurnK mb matches 4 run return run function rlk:mboss/azhdaha/yaw/play_turn90_r
execute if score #azTurnK mb matches 5 run return run function rlk:mboss/azhdaha/yaw/play_turn180
execute if score #azTurnK mb matches 6 run return run function rlk:mboss/azhdaha/yaw/play_turn180_m
