# 아주 작은 방: 무리 하나(5~6번째 맵은 창병 대열)
execute store result score #c2r tmp run random value 1..2
scoreboard players set #c2n tmp 4
execute if score #mapIdx room matches ..3 if score #c2r tmp matches 1 run return run function rlk:cm/c2/plan_add {id:"g_ns"}
scoreboard players set #c2n tmp 2
execute if score #mapIdx room matches ..3 run return run function rlk:cm/c2/plan_add {id:"g_sl"}
scoreboard players set #c2n tmp 3
function rlk:cm/c2/plan_add {id:"g_sp"}
