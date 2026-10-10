# 방패병: 정면 ±60° 공격은 방패 내구도가 대신 받음. 천천히 돎(뒤로 돌아 들어가면 맞음)
# 공격: 방패 휘두르기(가까이) / 선딜 후 돌진(장애물 파괴) + 끝에 휘두르기
execute unless score @s cmShM matches 1.. run function rlk:cm/sh/init
function rlk:cm/sh/bar
execute if score @s cmS matches 1 run return run function rlk:cm/sh/swing
execute if score @s cmS matches 2 run return run function rlk:cm/sh/rwind
execute if score @s cmS matches 3 run return run function rlk:cm/sh/rush
execute if score @s cmS matches 4 run return run function rlk:cm/sh/rswing
function rlk:cm/sh/turn
execute if score #free tmp matches 0 run return 0
execute if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..2.9] run return run function rlk:cm/sh/sstart
execute if score @s cmCd2 matches ..0 if entity @e[tag=rlk_body,distance=4.5..12] run function rlk:cm/sh/rstart
