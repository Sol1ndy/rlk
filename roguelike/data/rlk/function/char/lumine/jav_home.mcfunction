# 위치 = 투창의 4.5칸 앞. 그 지점에서 적 쪽으로 0.6칸 옮긴 곳을 바라보게 한다(틱당 최대 약 7도)
execute facing entity @e[tag=rlk_mob,distance=..4,sort=nearest,limit=1] eyes positioned ^ ^ ^0.6 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_aimpt"]}
execute at @s facing entity @e[tag=rlk_aimpt,limit=1] feet run tp @s ~ ~ ~ ~ ~
kill @e[tag=rlk_aimpt]
