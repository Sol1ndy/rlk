# @s = 마도서 페이지, at @s. 0.6초 동안 튀어 오른 뒤 몸에게 날아가 흡수된다. 몸이 너무 멀거나 없으면 그 자리에 머묾
particle minecraft:enchant ~ ~0.3 ~ 0.12 0.12 0.12 0.2 1
scoreboard players add @s life 1
execute if score @s life matches ..11 run return 0
execute if score @s life matches 12 run data merge entity @s {NoGravity:1b,Motion:[0.0d,0.0d,0.0d]}
execute if score @s life matches 2400.. run return run kill @s
execute unless entity @e[tag=rlk_body,distance=..40] run return 0
execute positioned ~ ~-1 ~ if entity @e[tag=rlk_body,distance=..1.2] run return run function rlk:items/proc/page_orb_absorb
execute facing entity @e[tag=rlk_body,limit=1] eyes run tp @s ^ ^ ^0.8
particle minecraft:end_rod ~ ~0.2 ~ 0.05 0.05 0.05 0.01 1
