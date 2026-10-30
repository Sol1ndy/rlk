# 2챕터 방 구성 (@s = 구역 표식, room/mob_wave 에서). #mobN(방 크기 규칙의 수) → 무리 목록 rlk:c2 plan, #mobN = 무리 수
data modify storage rlk:c2 plan set value []
scoreboard players operation #c2N tmp = #mobN tmp
execute if score #c2N tmp matches ..2 run function rlk:cm/c2/plan_small
execute if score #c2N tmp matches 3.. if score #mapIdx room matches ..1 run function rlk:cm/c2/plan_a
execute if score #c2N tmp matches 3.. if score #mapIdx room matches 2..3 run function rlk:cm/c2/plan_b
execute if score #c2N tmp matches 3.. if score #mapIdx room matches 4.. run function rlk:cm/c2/plan_c
execute store result score #mobN tmp run data get storage rlk:c2 plan
