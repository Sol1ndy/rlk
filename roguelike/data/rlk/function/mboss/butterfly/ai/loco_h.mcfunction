scoreboard players add #bfMvT mb 1
# walk in beyond 7 b, so most decisions fall in the mid band (every human pattern), not only the far one
execute unless entity @e[tag=rlk_body,distance=..7,limit=1] run return run function rlk:mboss/butterfly/ai/walk
execute if entity @e[tag=rlk_body,distance=..2.2,limit=1] run return run function rlk:mboss/butterfly/ai/backoff
function rlk:mboss/butterfly/ai/strafe
