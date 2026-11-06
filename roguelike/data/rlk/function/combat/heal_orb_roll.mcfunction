# 로비(튜토리얼 · 체험)의 더미 · 허수아비는 주지 않음
execute if entity @s[tag=rlk_lobby] run return 0
execute if entity @s[tag=rlk_c2lite] run return 0
# 처치 시 5% 확률 회복구슬 (@s = 몹, at @s)
execute store result score #hor tmp run random value 1..100
execute if score #hor tmp matches ..5 run function rlk:combat/heal_orb_spawn
