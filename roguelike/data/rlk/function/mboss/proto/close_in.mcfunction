# Melee pattern chosen from afar: dash toward the player (0.45 b/t) up to 30 ticks, then start.
scoreboard players add #prGoT mb 1
function rlk:mboss/mv/turn {max:30}
function rlk:mboss/mv/toward {d:0.45}
execute if entity @e[tag=rlk_body,distance=..3.6,limit=1] run scoreboard players set #prGo mb 0
execute if score #prGoT mb matches 30.. run scoreboard players set #prGo mb 0
