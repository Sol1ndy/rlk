# From rlk:tick, only while #mbLive mb is 1 (set by mboss/start and mboss/reload, cleared by cleanup_fight and
# here), so outside a fight the server never scans for mid-boss entities. No body any more (killed, /kill,
# lost): the fight's leftovers and the bars go, and the scans stop until the next mboss/start.
# Low gravity is a per-tick request: cleared here, set again by the running module's tick (#mbLowG mb 1), so a
# paused fight, a missing player or body, the intro, the death sequence and every exit path drop it at once.
scoreboard players set #mbLowG mb 0
execute if entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run return run function rlk:mboss/world
function rlk:mboss/cleanup_aux
function rlk:mboss/bars_hide
scoreboard players set #mbLive mb 0
