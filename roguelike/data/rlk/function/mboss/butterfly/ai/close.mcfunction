# @s = body, burst-running (12-16 m/s) for #bfPick: 0.7 b/t for at most 12 t, then the pattern starts.
scoreboard players add #bfT mb 1
function rlk:mboss/mv/turn {max:30}
function rlk:mboss/mv/toward {d:0.7}
scoreboard players operation #bfM mb = #bfT mb
scoreboard players operation #bfM mb %= #bfK2 mb
execute if score #bfM mb matches 0 run particle minecraft:poof ~ ~0.1 ~ 0.25 0.02 0.25 0.02 2 force @a[tag=player]
execute if score #bfPick mb matches 2 if entity @e[tag=rlk_body,distance=..3,limit=1] run return run function rlk:mboss/butterfly/ai/go
execute if score #bfT mb matches 12.. run function rlk:mboss/butterfly/ai/go
