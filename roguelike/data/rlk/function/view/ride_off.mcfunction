# F5 위쪽 시점을 떠날 때 (@s = 플레이어): 내려서 원래 크기로
ride @s dismount
attribute @s minecraft:scale base reset
kill @e[tag=rlk_vseat]
title @s clear
