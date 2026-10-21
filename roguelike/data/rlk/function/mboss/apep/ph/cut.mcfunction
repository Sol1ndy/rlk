# @s = body: stop whatever runs (hazards, the slot, chains, the yaw driver, the cine, a queued transition).
function rlk:mboss/apep/svc/lib_clear
function rlk:mboss/apep/p/cancel
function rlk:mboss/apep/dome/clear
scoreboard players set #apTr mb 0
scoreboard players set #apChP mb 0
scoreboard players set #apNext mb 0
scoreboard players set #apYawC mb 0
function rlk:mboss/apep/svc/cine_off
scoreboard players set #mbFloorHit mb 0
