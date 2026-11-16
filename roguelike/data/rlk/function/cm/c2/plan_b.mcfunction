# 3~4번째 맵: 무리 1~2 + 정예 하나(카이라기 · 시킨 술사) + 가끔(35%) 북잡이
execute store result score #c2r tmp run random value 1..2
scoreboard players set #c2n tmp 4
execute if score #c2N tmp matches 7.. run scoreboard players set #c2n tmp 5
execute if score #c2N tmp matches 5.. run function rlk:cm/c2/plan_add {id:"g_ns"}
execute if score #c2N tmp matches ..4 if score #c2r tmp matches 1 run function rlk:cm/c2/plan_add {id:"g_ns"}
scoreboard players set #c2n tmp 2
execute if score #c2N tmp matches 5.. run function rlk:cm/c2/plan_add {id:"g_sl"}
execute if score #c2N tmp matches ..4 if score #c2r tmp matches 2 run function rlk:cm/c2/plan_add {id:"g_sl"}
scoreboard players set #c2n tmp 1
execute store result score #c2r tmp run random value 1..2
execute if score #c2r tmp matches 1 run function rlk:cm/c2/plan_add {id:"kr"}
execute if score #c2r tmp matches 2 run function rlk:cm/c2/plan_add {id:"cc"}
execute store result score #c2r tmp run random value 1..100
execute if score #c2r tmp matches ..35 run function rlk:cm/c2/plan_add {id:"dr"}
