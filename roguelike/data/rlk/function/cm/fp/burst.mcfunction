# 터짐 (@s = 주머니, at @s): 반경 3 안의 맞힐 수 있는 커스텀 몹 두뇌에만(rlk_mob: 플레이어 · 땅속에 있는 전갈 새끼 · 성수 전갈 제외). 버섯 = 최대 체력 100 %(한 방에 무리째), 다른 몹 = 12 + 최대 체력 30 %. 한 몹은 한 틱에 주머니 하나만
execute as @e[tag=rlk_c3this] run function rlk:cm/fp/pose/50
particle minecraft:explosion ~ ~0.6 ~ 0 0 0 0 1 normal
particle minecraft:composter ~ ~0.6 ~ 1.4 0.5 1.4 0.3 40 normal
particle minecraft:spore_blossom_air ~ ~1 ~ 1.5 0.6 1.5 0 30 normal
particle minecraft:dust{color:[0.55,0.95,0.6],scale:2.0} ~ ~0.6 ~ 1.3 0.4 1.3 0 24 normal
execute unless score #c3fpburst snd matches 1 run function rlk:cm/c3/snd/fpburst
execute unless score #c3fpboom snd matches 1 run function rlk:cm/c3/snd/fpboom
execute as @e[tag=rlk_cmb,tag=rlk_mob,distance=..3] at @s run function rlk:cm/fp/blast_one
kill @e[tag=rlk_c3this]
kill @s
