# 4틱마다: 무리장을 찾고(없으면 내가 무리장), 1.8칸보다 멀면 무리장 쪽으로 끌림 → 무리가 한 덩어리로 뭉침
scoreboard players set @s c2T 4
scoreboard players operation #g tmp = @s c2G
execute as @e[tag=rlk_fu_lead,distance=..24] if score @s c2G = #g tmp run tag @s add rlk_c2ld
execute unless entity @e[tag=rlk_c2ld,limit=1] run tag @s add rlk_fu_lead
execute if entity @s[tag=rlk_fu_lead] run return run tag @e[tag=rlk_c2ld] remove rlk_c2ld
scoreboard players set #c2Fw tmp 240
scoreboard players set #c2Up tmp -1
execute unless entity @e[tag=rlk_c2ld,distance=..1.8] facing entity @e[tag=rlk_c2ld,limit=1,sort=nearest] feet rotated ~ 0 run function rlk:cm/c2/impulse
tag @e[tag=rlk_c2ld] remove rlk_c2ld
