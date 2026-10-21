# The proxy set parked (#apPx 6): the framework px/state (cm.md 9.3: inv sets toggle rlk_mb_inv through
# rlk_mb_pxinv); hidden (FN-13 / R10): the husk at scale 0.1 without its click shield.
scoreboard players set #apPx mb 6
function rlk:mboss/px/state {set:"parked"}
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/apep/u/hide_on
