# 아주 작은 방: 무리 하나. 우림 = 버섯 무리, 사막 = 전갈 새끼(5~6번째 맵은 용병 무리)
scoreboard players set #c3n tmp 5
execute if score #c3sd tmp matches 0 run return run function rlk:cm/c3/plan_add {id:"g_fu"}
scoreboard players set #c3n tmp 6
execute if score #mapIdx room matches ..3 run return run function rlk:cm/c3/plan_add {id:"g_sb"}
scoreboard players set #c3n tmp 3
function rlk:cm/c3/plan_add {id:"g_em"}
