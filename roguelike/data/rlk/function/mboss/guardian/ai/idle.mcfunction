# @s = body. Hover and track the player; glide closer while farther than 9 b (she never walks);
# decide when the cooldown is over.
function rlk:mboss/guardian/rig/face/track
execute if score #gdCool mb matches 1.. run scoreboard players remove #gdCool mb 1
execute unless entity @e[tag=rlk_body,distance=..9,limit=1] run function rlk:mboss/guardian/ai/drift
execute if score #gdMv mb matches 1 if entity @e[tag=rlk_body,distance=..8,limit=1] run function rlk:mboss/guardian/ai/hover
execute if score #gdCool mb matches ..0 run function rlk:mboss/guardian/ai/next
