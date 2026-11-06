# @s = body, closing in for #gdPick (glide 0.3 b/t, at most 30 t), then the pattern starts.
scoreboard players add #gdT mb 1
function rlk:mboss/mv/turn {max:30}
function rlk:mboss/mv/toward {d:0.3}
execute if score #gdPick mb matches 3 if entity @e[tag=rlk_body,distance=..3,limit=1] run return run function rlk:mboss/guardian/ai/go
execute if score #gdT mb matches 30.. run function rlk:mboss/guardian/ai/go
