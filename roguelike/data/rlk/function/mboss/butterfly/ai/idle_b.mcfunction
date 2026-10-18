# @s = body, butterfly form (she always hovers; the rig carries the height): track, glide in beyond 8 b at
# 0.25 b/t and out inside 3.5 b at 0.2 b/t (inside r 16.5: wx/u/toward|away), decide when the cooldown is over.
function rlk:mboss/butterfly/rig/face/track
execute if score #bfCool mb matches 1.. run scoreboard players remove #bfCool mb 1
function rlk:mboss/butterfly/ai/loco_b
execute if score #bfCool mb matches ..0 run function rlk:mboss/butterfly/ai/next
