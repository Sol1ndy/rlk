# 5틱마다: 무리장을 찾고(없으면 내가 무리장), 2.6칸보다 멀면 무리장 쪽으로 끌림
scoreboard players set @s c2T 5
scoreboard players operation #g tmp = @s c2G
execute as @e[tag=rlk_ns_lead,distance=..24] if score @s c2G = #g tmp run tag @s add rlk_c2ld
execute unless entity @e[tag=rlk_c2ld,limit=1] run tag @s add rlk_ns_lead
execute if entity @s[tag=rlk_ns_lead] run return run tag @e[tag=rlk_c2ld] remove rlk_c2ld
scoreboard players set #c2Fw tmp 230
scoreboard players set #c2Up tmp -1
execute unless entity @e[tag=rlk_c2ld,distance=..2.6] facing entity @e[tag=rlk_c2ld,limit=1,sort=nearest] feet rotated ~ 0 run function rlk:cm/c2/impulse
tag @e[tag=rlk_c2ld] remove rlk_c2ld
