# 전투 중 매 틱: 소환 대기 → 적이 모두 죽으면 정리
execute if score #spawnT room matches 1.. run return run function rlk:room/combat_wait
execute unless entity @e[tag=rlk_zmob,limit=1] as @e[tag=rlk_zone] if score @s zid = #combat room at @s run function rlk:room/combat_clear
