# 슬라임이 터짐 (@s = 뿌리, at @s): 2칸 안의 다른 슬라임 두뇌에만 방전(플레이어는 대상이 아님)
particle minecraft:electric_spark ~ ~0.5 ~ 1.0 0.3 1.0 0.25 24 normal
execute unless score #c2zap snd matches 1 run function rlk:cm/c2/snd/zap
execute as @e[tag=rlk_c2slime,tag=rlk_cmb,distance=..2] at @s run function rlk:cm/c2/zap_one
