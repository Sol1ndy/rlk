# 새 두뇌 마무리 (@e[tag=rlk_cmnew]): cmId, 실행 방향을 두뇌의 방향으로, cm/init
scoreboard players add #cmIdC tmp 1
scoreboard players operation @e[tag=rlk_cmnew] cmId = #cmIdC tmp
tp @e[tag=rlk_cmnew] ~ ~ ~ ~ 0
execute as @e[tag=rlk_cmnew] at @s run function rlk:cm/init
