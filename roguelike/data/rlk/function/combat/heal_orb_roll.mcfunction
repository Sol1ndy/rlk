# 처치 시 5% 확률 회복구슬 (@s = 몹, at @s)
execute store result score #hor tmp run random value 1..100
execute if score #hor tmp matches ..5 run function rlk:combat/heal_orb_spawn
