# 따라붙을 대상 찾기 (위치 = 눈, 방향 = 조준)
execute unless entity @e[tag=rlk_artg,limit=1] positioned ^ ^ ^2 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..0.88,sort=nearest,limit=1] add rlk_artg
execute unless entity @e[tag=rlk_artg,limit=1] positioned ^ ^ ^4 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..1.16,sort=nearest,limit=1] add rlk_artg
execute unless entity @e[tag=rlk_artg,limit=1] positioned ^ ^ ^6 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..1.44,sort=nearest,limit=1] add rlk_artg
execute unless entity @e[tag=rlk_artg,limit=1] positioned ^ ^ ^8 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..1.72,sort=nearest,limit=1] add rlk_artg
execute unless entity @e[tag=rlk_artg,limit=1] positioned ^ ^ ^10 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..2.00,sort=nearest,limit=1] add rlk_artg
execute unless entity @e[tag=rlk_artg,limit=1] positioned ^ ^ ^12 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..2.28,sort=nearest,limit=1] add rlk_artg
