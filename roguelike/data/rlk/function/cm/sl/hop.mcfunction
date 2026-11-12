# 깡충 (땅에 있을 때만): 몸 쪽으로 0.26 칸/틱, 위로 0.4
scoreboard players operation @s c2T = #c2Hop_sl tmp
execute unless data entity @s {OnGround:1b} run return 0
scoreboard players set @s c2T2 8
scoreboard players set #c2Fw tmp 260
scoreboard players set #c2Up tmp 400
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:cm/c2/impulse
execute unless score #c2sljump snd matches 1 run function rlk:cm/c2/snd/sljump
