# 터짐: 연기 · 모래 · 풀빛 포자 · 소리, 부품 제거
particle minecraft:poof ~ ~0.7 ~ 0.3 0.35 0.3 0.05 12 normal
particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.5 ~ 0.35 0.3 0.35 0.1 14 normal
particle minecraft:composter ~ ~0.8 ~ 0.35 0.4 0.35 0.1 10 normal
particle minecraft:crit ~ ~0.9 ~ 0.3 0.4 0.3 0.4 8 normal
execute unless score #c3pop snd matches 1 run function rlk:cm/c3/snd/pop
kill @e[tag=rlk_c3this]
