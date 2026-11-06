scoreboard players add #gdT mb 1
function rlk:mboss/guardian/rig/face/track
function rlk:mboss/mv/toward {d:0.15}
execute if entity @e[tag=rlk_body,distance=..2.5,limit=1] run return run function rlk:mboss/guardian/ai/approach_end
execute if score #gdT mb matches 40.. run function rlk:mboss/guardian/ai/approach_end
