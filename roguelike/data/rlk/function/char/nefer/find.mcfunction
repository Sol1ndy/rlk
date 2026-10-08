# 그림자가 노릴 적 (위치 = 눈, 방향 = 조준): 조준선을 따라 8칸까지
execute unless entity @e[tag=rlk_nftg,limit=1] positioned ^ ^ ^2 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..0.88,sort=nearest,limit=1] add rlk_nftg
execute unless entity @e[tag=rlk_nftg,limit=1] positioned ^ ^ ^4 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..1.16,sort=nearest,limit=1] add rlk_nftg
execute unless entity @e[tag=rlk_nftg,limit=1] positioned ^ ^ ^6 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..1.44,sort=nearest,limit=1] add rlk_nftg
execute unless entity @e[tag=rlk_nftg,limit=1] positioned ^ ^ ^8 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..1.72,sort=nearest,limit=1] add rlk_nftg
