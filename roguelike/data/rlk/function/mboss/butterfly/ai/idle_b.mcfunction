# @s = body, butterfly form (she always hovers; the rig carries the height): track, keep 5-8 b (gliding
# in at 0.25 b/t, out at 0.2 b/t), decide when the cooldown is over.
function rlk:mboss/butterfly/rig/face/track
execute if score #bfCool mb matches 1.. run scoreboard players remove #bfCool mb 1
function rlk:mboss/butterfly/ai/loco_b
execute if score #bfCool mb matches ..0 run function rlk:mboss/butterfly/ai/next
