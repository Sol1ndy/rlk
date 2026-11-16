# 터짐: 연기 · 번개 불꽃 · 소리, 부품 제거
particle minecraft:poof ~ ~0.8 ~ 0.3 0.4 0.3 0.06 14 normal
particle minecraft:electric_spark ~ ~0.8 ~ 0.35 0.45 0.35 0.35 12 normal
particle minecraft:crit ~ ~0.9 ~ 0.3 0.4 0.3 0.4 10 normal
execute unless score #c2pop snd matches 1 run function rlk:cm/c2/snd/pop
kill @e[tag=rlk_c2this]
