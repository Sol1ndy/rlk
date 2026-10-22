# The proxy set p3c (#apPx 2): the framework px/state (cm.md 9.3: inv sets toggle rlk_mb_inv through
# rlk_mb_pxinv); visible: the husk back at the registry scale with its torso click shield.
scoreboard players set #apPx mb 2
function rlk:mboss/px/state {set:"p3c"}
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:boss/apep/u/hide_off
