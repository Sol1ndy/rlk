# 1~2번째 맵: 우림 = 버섯 무리 둘, 사막 = 전갈 새끼 무리 + 용병 무리 (방이 클수록 무리가 커짐)
execute if score #c3sd tmp matches 1 run return run function rlk:cm/c3/plan_a_d
scoreboard players set #c3n tmp 5
execute if score #c3N tmp matches 6.. run scoreboard players set #c3n tmp 6
execute if score #c3N tmp matches 8.. run scoreboard players set #c3n tmp 7
function rlk:cm/c3/plan_add {id:"g_fu"}
scoreboard players set #c3n tmp 5
execute if score #c3N tmp matches 7.. run scoreboard players set #c3n tmp 6
function rlk:cm/c3/plan_add {id:"g_fu"}
