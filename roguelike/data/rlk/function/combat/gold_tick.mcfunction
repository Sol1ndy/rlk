# @s = 골드 조각, at @s. 0.6초 동안 튀어 오른 뒤 몸(아바타)에게 날아가 흡수된다. 몸이 너무 멀거나 없으면 그 자리에 머묾
scoreboard players add @s life 1
execute if score @s life matches ..11 run return 0
execute if score @s life matches 12 run data merge entity @s {NoGravity:1b,Motion:[0.0d,0.0d,0.0d]}
execute if score @s life matches 2400.. run return run kill @s
execute unless entity @e[tag=rlk_body,distance=..40] run return 0
execute positioned ~ ~-1 ~ if entity @e[tag=rlk_body,distance=..1.2] run return run function rlk:combat/gold_absorb
execute facing entity @e[tag=rlk_body,limit=1] eyes run tp @s ^ ^ ^0.8
particle minecraft:wax_on ~ ~0.2 ~ 0.05 0.05 0.05 0 1
