# 5~6번째 맵: 창병 대열 + 졸개 무리 + 정예 하나(그림자 닌자 50%, 카이라기 · 시킨 술사 25%씩) + 북잡이 60%, 아주 큰 방은 슬라임도
scoreboard players set #c2n tmp 3
function rlk:cm/c2/plan_add {id:"g_sp"}
scoreboard players set #c2n tmp 4
execute if score #c2N tmp matches 7.. run scoreboard players set #c2n tmp 5
function rlk:cm/c2/plan_add {id:"g_ns"}
scoreboard players set #c2n tmp 1
execute store result score #c2r tmp run random value 1..4
execute if score #c2r tmp matches 1..2 run function rlk:cm/c2/plan_add {id:"nj"}
execute if score #c2r tmp matches 3 run function rlk:cm/c2/plan_add {id:"kr"}
execute if score #c2r tmp matches 4 run function rlk:cm/c2/plan_add {id:"cc"}
execute store result score #c2r tmp run random value 1..100
execute if score #c2r tmp matches ..60 run function rlk:cm/c2/plan_add {id:"dr"}
scoreboard players set #c2n tmp 2
execute if score #c2N tmp matches 8.. run function rlk:cm/c2/plan_add {id:"g_sl"}
