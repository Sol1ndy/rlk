# The proxy set dead (#apPx 7): the framework px/state (cm.md 9.3: inv sets toggle rlk_mb_inv through
# rlk_mb_pxinv); visible: the husk back at the registry scale with its torso click shield.
scoreboard players set #apPx mb 7
function rlk:mboss/px/state {set:"dead"}
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/apep/u/hide_off
