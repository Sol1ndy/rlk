# @s = 플레이어, at @s. 변신 소리 + 나선 이펙트 타이머 시작(메시지 없음)
scoreboard players set @s kirionFxT 30
execute unless score #k184 snd matches 1 run function rlk:snd/f199
execute unless score #k185 snd matches 1 run function rlk:snd/f200
execute unless score #k186 snd matches 1 run function rlk:snd/f201
particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.02 20
