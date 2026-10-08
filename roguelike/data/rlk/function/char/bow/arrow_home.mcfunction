# 위치 = 화살의 2칸 앞. 거기서 가장 가까운 적 쪽으로 1.2칸 옮긴 곳을 바라보게 한다(틱당 최대 약 30도)
execute facing entity @e[tag=rlk_mob,distance=..24,sort=nearest,limit=1] eyes positioned ^ ^ ^1.2 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_aimpt"]}
execute at @s facing entity @e[tag=rlk_aimpt,limit=1] feet run tp @s ~ ~ ~ ~ ~
kill @e[tag=rlk_aimpt]
