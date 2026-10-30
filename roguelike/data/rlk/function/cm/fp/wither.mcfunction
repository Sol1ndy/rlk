# 3초 동안 아무도 안 건드림: 쪼그라들며 사라짐(피해 없음)
particle minecraft:poof ~ ~0.4 ~ 0.2 0.2 0.2 0.02 6 normal
execute unless score #c3fpwither snd matches 1 run function rlk:cm/c3/snd/fpwither
kill @e[tag=rlk_c3this]
kill @s
