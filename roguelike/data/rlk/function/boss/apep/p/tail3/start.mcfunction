# 생명의 꼬리 (tail3, id 34; plan 8.3 Q4): crouch_p3 (the core plays it at 0), the walk opener when the player
# is farther than 8.0 b (#apq34 1: walk_p3 <= 30 t at 0.2 b/t), then tail_p3 at #apq34T 0.
kill @e[tag=rlk_mb_ap_p34]
function rlk:mboss/mv/dist
scoreboard players set #apq34 mb 0
execute if score #mbDist mb matches 81.. run scoreboard players set #apq34 mb 1
scoreboard players set #apq34O mb 8
execute if score #apq34 mb matches 1 run scoreboard players set #apq34O mb 38
scoreboard players set #apPLen mb 95
execute if score #apq34 mb matches 1 run scoreboard players set #apPLen mb 125
scoreboard players operation #apq34T mb = #apPT mb
scoreboard players operation #apq34T mb -= #apq34O mb
