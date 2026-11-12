# 3~6번째 맵의 바탕: 무리 둘(우림 = 버섯 + 용병, 사막 = 전갈 새끼 + 용병) + 3~4번째 맵은 정예 하나(우림 = 재구성자, 사막 = 성수 전갈 · 독수리 반반)
scoreboard players set #c3n tmp 5
execute if score #c3N tmp matches 7.. run scoreboard players set #c3n tmp 6
execute if score #c3sd tmp matches 0 run function rlk:cm/c3/plan_add {id:"g_fu"}
scoreboard players set #c3n tmp 6
execute if score #c3N tmp matches 7.. run scoreboard players set #c3n tmp 7
execute if score #c3sd tmp matches 1 run function rlk:cm/c3/plan_add {id:"g_sb"}
scoreboard players set #c3n tmp 3
execute if score #c3N tmp matches 6.. run scoreboard players set #c3n tmp 4
function rlk:cm/c3/plan_add {id:"g_em"}
execute if score #mapIdx room matches 4.. run return 0
scoreboard players set #c3n tmp 1
execute if score #c3sd tmp matches 0 run return run function rlk:cm/c3/plan_add {id:"pc"}
execute store result score #c3r tmp run random value 1..2
execute if score #c3r tmp matches 1 run function rlk:cm/c3/plan_add {id:"cs"}
execute if score #c3r tmp matches 2 run function rlk:cm/c3/plan_add {id:"rv"}
