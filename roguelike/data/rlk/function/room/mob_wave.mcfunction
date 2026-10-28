# 적 소환 (@s = 구역 표식, at @s). 수 = 구역 크기별 범위 + (챕터 - 1)
execute if score @s zkind matches 9 run return run function rlk:room/boss_spawn
# 중간보스 구역: 몹 대신 원형 경기장의 중간보스(mboss/start, 실패하면 #spawnT 로 다시 시도)
execute if score @s zkind matches 15 run return run function rlk:mboss/start
function rlk:room/mob_count with entity @s data
scoreboard players operation #mobN tmp += #chapter room
scoreboard players remove #mobN tmp 1
execute if score #chapter room matches 2 unless score #mobTmp room matches 1 run function rlk:cm/c2/plan
function rlk:room/mob_loop
