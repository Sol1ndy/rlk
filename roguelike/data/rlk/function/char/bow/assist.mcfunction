# 조준 보정 (@s = 방금 만든 화살, at @s = 눈 위치·조준 방향). 조준선을 2칸씩 따라가며, 그 지점(몸통 높이로 1칸 내림)에서 반경 0.6 + 거리×0.14 칸 안의 적을 찾는다(24칸까지)
# 숫자를 키우면 더 너그럽게, 줄이면 더 정확히 겨눠야 한다 (build/p77 의 BASE · SLOPE)
execute unless entity @e[tag=rlk_ast,limit=1] positioned ^ ^ ^2 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..0.88,sort=nearest,limit=1] add rlk_ast
execute unless entity @e[tag=rlk_ast,limit=1] positioned ^ ^ ^4 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..1.16,sort=nearest,limit=1] add rlk_ast
execute unless entity @e[tag=rlk_ast,limit=1] positioned ^ ^ ^6 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..1.44,sort=nearest,limit=1] add rlk_ast
execute unless entity @e[tag=rlk_ast,limit=1] positioned ^ ^ ^8 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..1.72,sort=nearest,limit=1] add rlk_ast
execute unless entity @e[tag=rlk_ast,limit=1] positioned ^ ^ ^10 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..2.00,sort=nearest,limit=1] add rlk_ast
execute unless entity @e[tag=rlk_ast,limit=1] positioned ^ ^ ^12 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..2.28,sort=nearest,limit=1] add rlk_ast
execute unless entity @e[tag=rlk_ast,limit=1] positioned ^ ^ ^14 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..2.56,sort=nearest,limit=1] add rlk_ast
execute unless entity @e[tag=rlk_ast,limit=1] positioned ^ ^ ^16 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..2.84,sort=nearest,limit=1] add rlk_ast
execute unless entity @e[tag=rlk_ast,limit=1] positioned ^ ^ ^18 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..3.12,sort=nearest,limit=1] add rlk_ast
execute unless entity @e[tag=rlk_ast,limit=1] positioned ^ ^ ^20 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..3.40,sort=nearest,limit=1] add rlk_ast
execute unless entity @e[tag=rlk_ast,limit=1] positioned ^ ^ ^22 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..3.68,sort=nearest,limit=1] add rlk_ast
execute unless entity @e[tag=rlk_ast,limit=1] positioned ^ ^ ^24 positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..3.96,sort=nearest,limit=1] add rlk_ast
execute if entity @e[tag=rlk_ast,limit=1] facing entity @e[tag=rlk_ast,limit=1] eyes run tp @s ~ ~ ~ ~ ~
tag @e[tag=rlk_ast] remove rlk_ast
