# 로비(튜토리얼 · 체험)의 더미 · 허수아비는 주지 않음
execute if entity @s[tag=rlk_lobby] run return 0
# 처치 경험치 (@s = 죽는 몹). 몹에 xpDrop 스코어가 있으면 그 값, 없으면 #killXp
scoreboard players operation #xpAdd tmp = #killXp tmp
execute if score @s xpDrop matches 0.. run scoreboard players operation #xpAdd tmp = @s xpDrop
execute if score #xpAdd tmp matches 1.. as @a[tag=player,limit=1] run function rlk:player/level/add_xp
