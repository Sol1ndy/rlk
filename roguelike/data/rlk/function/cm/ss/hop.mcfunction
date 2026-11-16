# 깡충 (땅에 있을 때만): 몸 쪽으로 0.33 칸/틱, 위로 0.33
scoreboard players operation @s c2T = #c2Hop_ss tmp
execute unless data entity @s {OnGround:1b} run return 0
scoreboard players set @s c2T2 8
scoreboard players set #c2Fw tmp 330
scoreboard players set #c2Up tmp 330
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:cm/c2/impulse
execute unless score #c2ssjump snd matches 1 run function rlk:cm/c2/snd/ssjump
