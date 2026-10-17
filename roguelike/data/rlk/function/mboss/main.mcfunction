# From rlk:tick, only while #mbLive mb is 1 (set by mboss/start and mboss/reload, cleared by cleanup_fight and
# here), so outside a fight the server never scans for mid-boss entities. No body any more (killed, /kill,
# lost): the fight's leftovers and the bars go, and the scans stop until the next mboss/start.
execute if entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run return run function rlk:mboss/world
function rlk:mboss/cleanup_aux
function rlk:mboss/bars_hide
scoreboard players set #mbLive mb 0
