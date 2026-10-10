# 로비 방 안 (@s = 플레이어)
# 런이 시작됐으면 로비 상태 끝
execute if score #active room matches 1 run return run function rlk:lobby/leave
# 선택 공간(도감 등)에 가 있는 동안은 쉰다
execute if score @s pkMode matches 1.. run return 0
# 오브젝트 조준
tag @e[tag=rlk_lhover] remove rlk_lhover
execute at @s if entity @e[tag=rlk_lobj,distance=..20] anchored eyes positioned ^ ^ ^0.01 anchored feet run function rlk:lobby/obj/aim
execute at @s as @e[tag=rlk_lobj,distance=..22] run function rlk:lobby/obj/hover
execute if score @s lobRoom matches 2 run function rlk:lobby/tut/tick
execute if score @s lobRoom matches 4 run function rlk:lobby/try/tick
