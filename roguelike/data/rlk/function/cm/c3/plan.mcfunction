# 3챕터 방 구성 (@s = 구역 표식, room/mob_wave 에서). #mobN(방 크기 규칙의 수) → 무리 목록 rlk:c3 plan, #mobN = 무리 수.
# 구역 data.sd 1 = 사막(모래 전갈 새끼 · 성수 전갈), 0 = 우림(둥실 버섯 · 재구성자). 정예 id 는 실행 시점에 부름
data modify storage rlk:c3 plan set value []
scoreboard players operation #c3N tmp = #mobN tmp
execute store result score #c3sd tmp run data get entity @s data.sd
execute if score #c3N tmp matches ..2 run function rlk:cm/c3/plan_small
execute if score #c3N tmp matches 3.. if score #mapIdx room matches ..1 run function rlk:cm/c3/plan_a
execute if score #c3N tmp matches 3.. if score #mapIdx room matches 2.. run function rlk:cm/c3/plan_b
execute if score #c3N tmp matches 3.. if score #mapIdx room matches 4.. run function rlk:cm/c3/plan_c
execute store result score #mobN tmp run data get storage rlk:c3 plan
