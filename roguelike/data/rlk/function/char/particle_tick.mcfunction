# @s = 원소 입자, at @s. 0.3초 동안 흩어진 뒤 플레이어 쪽으로 날아가 흡수됨
scoreboard players add @s life 1
execute if score @s life matches 200.. run return run kill @s
execute if score @s life matches ..6 run return run tp @s ^ ^ ^0.32
execute unless entity @e[tag=rlk_body,distance=..48] run return run kill @s
execute facing entity @e[tag=rlk_body,limit=1] eyes run tp @s ^ ^ ^0.95
execute at @s positioned ~ ~-1 ~ if entity @e[tag=rlk_body,distance=..1.3] run function rlk:char/particle_absorb
