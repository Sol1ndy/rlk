# 조준 중 (@s = 플레이어, at 몸): 주변 결정 조각을 끌어당겨 줍는다. 우클릭 신호가 6틱 끊기면(뗌) 또는 5초가 지나면 발사
execute if score @s dead matches 1 run return run function rlk:char/navia/aim_cancel
execute if score @s pkMode matches 1.. run return run function rlk:char/navia/aim_cancel
scoreboard players add @s nvA 1
scoreboard players add @s nvGap 1
function rlk:char/navia/gun_follow
execute as @e[tag=rlk_crystal,distance=..12] at @s run function rlk:char/navia/pull
execute if score @s nvA matches 2.. run particle minecraft:wax_on ^ ^1 ^1 0.4 0.4 0.4 0 1
# 조준 진입 모션(skill_aim_in: 두 바퀴 돌며 우산을 머리 위로 돌리는 16틱) 중에 떼면, 조준 자세에 닿을 때까지(16틱 → skill_aim) 기다렸다 쏜다.
# 돌던 몸이 발사 모션(skill_fire 0틱 = 조준 자세)으로 2틱 만에 확 꺾이지 않게. 5초 제한(nvA 100)은 그대로
execute if score @s nvGap matches 6.. if score @s pmActive matches 1 if data storage rlk:player_motion active{clip:"skill_aim_in"} if score @s nvA matches ..99 run return 0
execute if score @s nvGap matches 6.. run return run function rlk:char/navia/aim_release
execute if score @s nvA matches 100.. run function rlk:char/navia/aim_release
