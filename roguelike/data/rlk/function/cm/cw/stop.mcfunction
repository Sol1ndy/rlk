# 영창 끝(치유할 몹이 없음 · 경직 · 빙결 · 끊김)
execute unless score @s cmS matches 1 run return 0
scoreboard players set @s cmS 0
execute as @e[tag=rlk_cw_orb,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {Glowing:0b}
