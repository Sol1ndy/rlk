# STUB (AP-CORE, ap_contract 1.3): 생명의 꼬리 (tail3, id 34); the pattern stage replaces this file.
# the walk opener when the player is farther than 8 b (#apq34 1); the expected end on #apPLen.
function rlk:mboss/mv/dist
scoreboard players set #apq34 mb 0
execute if score #mbDist mb matches 81.. run scoreboard players set #apq34 mb 1
scoreboard players set #apPLen mb 95
execute if score #apq34 mb matches 1 run scoreboard players set #apPLen mb 125
