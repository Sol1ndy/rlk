# @s = body: stop whatever runs (hazards, slots, the B3 special, fields, orbs, timers, a transition) and re-derive a
# clean state for the current phase (floor, proxies, rig, cine off).
function rlk:mboss/lib_clear
function rlk:mboss/azhdaha/p/cancel
function rlk:mboss/azhdaha/cast/cancel
function rlk:mboss/azhdaha/bg/cancel_l
function rlk:mboss/azhdaha/bg/cancel_t
function rlk:mboss/azhdaha/b3/special_cancel
function rlk:mboss/azhdaha/fld/clear
kill @e[tag=rlk_mb_az_orb]
kill @e[tag=rlk_mb_az_orbc]
function rlk:mboss/azhdaha/aft/clear
function rlk:mboss/azhdaha/fx/tele/clear
function rlk:mboss/azhdaha/svc/cine_off
function rlk:mboss/azhdaha/rig/glow/gold_off
scoreboard players set #azTr mb 0
scoreboard players set #azTrN mb 0
scoreboard players set #azBur mb 0
scoreboard players set #azOrbHigh mb 0
scoreboard players set #azLastHit mb 0
scoreboard players set #mbNoLeash mb 0
scoreboard players set #azCastFirst mb 0
execute if score #azPh mb matches 1 run function rlk:mboss/azhdaha/svc/floor_f1
execute if score #azPh mb matches 2 run function rlk:mboss/azhdaha/svc/floor_f2
execute if score #azPh mb matches 3 run function rlk:mboss/azhdaha/svc/floor_0
function rlk:mboss/azhdaha/px/normal
function rlk:mboss/azhdaha/rig/play/idle
scoreboard players set #azCool mb 10
scoreboard players set #azHudQ mb 1
