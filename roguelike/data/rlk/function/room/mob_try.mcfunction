# 구역의 칸 하나를 골라 그 안의 무작위 자리. 플레이어와 너무 가깝거나, 낙사 구간·장애물 자리면 다시. 끝내 못 찾으면 구역 한가운데
scoreboard players set #placed tmp 0
scoreboard players add #try tmp 1
execute if score #try tmp matches 16.. run return run function rlk:room/mob_summon
function rlk:room/mob_cell with entity @s data
function rlk:room/mob_cell2 with storage rlk:room a
function rlk:room/mob_pos with storage rlk:room sc
function rlk:room/mob_at with storage rlk:room sp
execute if score #placed tmp matches 0 run function rlk:room/mob_try
