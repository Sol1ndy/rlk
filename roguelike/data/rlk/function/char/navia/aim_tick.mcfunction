# 조준 중 (@s = 플레이어, at 몸): 주변 결정 조각을 끌어당겨 줍는다. 우클릭 신호가 6틱 끊기면(뗌) 또는 5초가 지나면 발사
execute if score @s dead matches 1 run return run function rlk:char/navia/aim_cancel
execute if score @s pkMode matches 1.. run return run function rlk:char/navia/aim_cancel
scoreboard players add @s nvA 1
scoreboard players add @s nvGap 1
function rlk:char/navia/gun_follow
execute as @e[tag=rlk_crystal,distance=..12] at @s run function rlk:char/navia/pull
execute if score @s nvA matches 2.. run particle minecraft:wax_on ^ ^1 ^1 0.4 0.4 0.4 0 1
execute if score @s nvGap matches 6.. run return run function rlk:char/navia/aim_release
execute if score @s nvA matches 100.. run function rlk:char/navia/aim_release
