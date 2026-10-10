# 포탄이 떨어지는 모습 (위치 = 맞는 자리): 비스듬히 위(9칸)에서 내려오는 빛줄기 + 폭발
scoreboard players set #sn tmp 0
execute positioned ~3 ~9 ~3 facing entity @s feet run function rlk:char/navia/shell_line
particle minecraft:explosion ~ ~0.8 ~ 0.3 0.2 0.3 0 2
particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.5 ~ 0.8 0.3 0.8 0.15 16
particle minecraft:small_flame ~ ~0.5 ~ 0.6 0.3 0.6 0.04 8
execute unless score #k64 snd matches 1 run function rlk:snd/f253
