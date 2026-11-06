# @s = body, human form (grounded): track the player; walk in when far, back off at walking pace when she is
# crowded, short strafing steps otherwise; decide when the cooldown is over.
function rlk:mboss/butterfly/rig/face/track
execute if score #bfCool mb matches 1.. run scoreboard players remove #bfCool mb 1
function rlk:mboss/butterfly/ai/loco_h
execute if score #bfCool mb matches ..0 run function rlk:mboss/butterfly/ai/next
