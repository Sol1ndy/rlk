# 적 소환 (@s = 구역 표식, at @s). 수 = 구역 크기별 범위 + (챕터 - 1)
execute if score @s zkind matches 9 run return run function rlk:room/boss_spawn
function rlk:room/mob_count with entity @s data
scoreboard players operation #mobN tmp += #chapter room
scoreboard players remove #mobN tmp 1
function rlk:room/mob_loop
