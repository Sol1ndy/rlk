# @s = 페이지 오브. 가장 가까운 플레이어가 흡수 → 금단의 도서 보유 시 페이지 +1
execute as @a[tag=player,limit=1] run function rlk:items/proc/page_orb_gain
particle minecraft:witch ~ ~0.5 ~ 0.3 0.3 0.3 0.3 12
execute unless score #k165 snd matches 1 run function rlk:snd/f174
execute unless score #k166 snd matches 1 run function rlk:snd/f175
execute unless score #k30 snd matches 1 run function rlk:snd/f176
execute unless score #k167 snd matches 1 run function rlk:snd/f177
kill @s
