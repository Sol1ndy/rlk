# @s = 인형, at @s. 주변(10칸) 적이 인형을 노리게: 인형이 0 피해를 준 것으로 처리
tag @s add rlk_dsrc
execute as @e[tag=rlk_mob,distance=..10] run damage @s 0 minecraft:generic by @e[tag=rlk_dsrc,limit=1]
tag @s remove rlk_dsrc
