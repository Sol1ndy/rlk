# 결정 조각을 몸 쪽으로 (@s = 결정 조각): 지나간 자리에 빛줄기, 몸에 닿으면 element/crystal_tick 이 줍는다
particle minecraft:wax_on ~ ~0.3 ~ 0.1 0.1 0.1 0 2
execute facing entity @e[tag=rlk_body,limit=1] feet run tp @s ^ ^ ^1.2
