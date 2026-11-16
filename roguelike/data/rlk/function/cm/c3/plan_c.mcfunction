# 5~6번째 맵: plan_b 의 무리 둘 + 정예 둘(우림 = 재구성자 + 독수리, 사막 = 성수 전갈 + 독수리) + 맑은물 술사
scoreboard players set #c3n tmp 1
execute if score #c3sd tmp matches 0 run function rlk:cm/c3/plan_add {id:"pc"}
execute if score #c3sd tmp matches 1 run function rlk:cm/c3/plan_add {id:"cs"}
function rlk:cm/c3/plan_add {id:"rv"}
function rlk:cm/c3/plan_add {id:"cw"}
