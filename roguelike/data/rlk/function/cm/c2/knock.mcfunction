# 몸에서 멀어지는 쪽으로 #c2KB(칸/틱 x1000) + 땅에 있으면 살짝 띄움
execute unless entity @e[tag=rlk_body,limit=1] run return 0
scoreboard players operation #c2Fw tmp = #c2KB tmp
scoreboard players set #c2Up tmp -1
execute if data entity @s {OnGround:1b} run scoreboard players set #c2Up tmp 220
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 run function rlk:cm/c2/impulse
