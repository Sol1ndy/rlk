# Hook death_start (@s = body; the framework cleared its libraries, hid the bars, set the proxies dead and stopped
# the music): every slot, the B3 special, the fields, orbs, timers, shards and the brand go; the arena fades back to
# Geo; the death clip and seq/death.
function rlk:boss/azhdaha/p/cancel
function rlk:boss/azhdaha/cast/cancel
function rlk:boss/azhdaha/bg/cancel_l
function rlk:boss/azhdaha/bg/cancel_t
function rlk:boss/azhdaha/b3/special_cancel
function rlk:boss/azhdaha/fld/clear
kill @e[tag=rlk_mb_az_orb]
kill @e[tag=rlk_mb_az_orbc]
function rlk:boss/azhdaha/aft/clear
function rlk:boss/azhdaha/brand/clear_all
kill @e[tag=rlk_mb_az_pat]
kill @e[tag=rlk_mb_az_seal]
function rlk:boss/azhdaha/fx/tele/clear
function rlk:boss/azhdaha/fx/tele/field_clear
function rlk:boss/azhdaha/fx/hud/clear
function rlk:boss/azhdaha/svc/cine_off
scoreboard players set #mbFloor mb 0
scoreboard players set #azTr mb 0
scoreboard players set #azBur mb 0
scoreboard players set #azPh mb 9
scoreboard players set #azLastHit mb 0
function rlk:boss/azhdaha/arena/look_geo
function rlk:boss/azhdaha/rig/glow/gold_off
function rlk:boss/azhdaha/rig/play/death
function rlk:boss/azhdaha/seq/death/start
