# 버섯이 죽음 (@s = 뿌리 = 두뇌가 있던 바닥): 부풀어 터지고, 그 자리에 포자 주머니(3초). 포자 폭발로 죽은 버섯은 주머니를 남기지 않음
function rlk:cm/fu/rig/pose/50
particle minecraft:spore_blossom_air ~ ~1 ~ 0.4 0.3 0.4 0 12 normal
execute unless score #c3fudie snd matches 1 run function rlk:cm/c3/snd/fudie
execute unless entity @s[tag=rlk_c3nopod] run function rlk:cm/fp/spawn
