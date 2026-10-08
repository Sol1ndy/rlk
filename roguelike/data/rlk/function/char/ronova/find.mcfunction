# 사형 선고 대상 찾기 (위치 = 눈, 방향 = 조준): 조준선을 2칸씩 20칸까지 따라가며 가까운 적(멀수록 너그럽게)
execute unless entity @e[tag=rlk_rntg,limit=1] positioned ^ ^ ^2 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..0.88,sort=nearest,limit=1] add rlk_rntg
execute unless entity @e[tag=rlk_rntg,limit=1] positioned ^ ^ ^4 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..1.16,sort=nearest,limit=1] add rlk_rntg
execute unless entity @e[tag=rlk_rntg,limit=1] positioned ^ ^ ^6 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..1.44,sort=nearest,limit=1] add rlk_rntg
execute unless entity @e[tag=rlk_rntg,limit=1] positioned ^ ^ ^8 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..1.72,sort=nearest,limit=1] add rlk_rntg
execute unless entity @e[tag=rlk_rntg,limit=1] positioned ^ ^ ^10 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..2.00,sort=nearest,limit=1] add rlk_rntg
execute unless entity @e[tag=rlk_rntg,limit=1] positioned ^ ^ ^12 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..2.28,sort=nearest,limit=1] add rlk_rntg
execute unless entity @e[tag=rlk_rntg,limit=1] positioned ^ ^ ^14 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..2.56,sort=nearest,limit=1] add rlk_rntg
execute unless entity @e[tag=rlk_rntg,limit=1] positioned ^ ^ ^16 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..2.84,sort=nearest,limit=1] add rlk_rntg
execute unless entity @e[tag=rlk_rntg,limit=1] positioned ^ ^ ^18 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..3.12,sort=nearest,limit=1] add rlk_rntg
execute unless entity @e[tag=rlk_rntg,limit=1] positioned ^ ^ ^20 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..3.40,sort=nearest,limit=1] add rlk_rntg
