# @s = body: stop whatever runs (hazards, slots, the B3 special, fields, orbs, timers, a transition) and re-derive a
# clean state for the current phase (floor, proxies, rig, cine off).
function rlk:mboss/lib_clear
function rlk:boss/azhdaha/p/cancel
function rlk:boss/azhdaha/cast/cancel
function rlk:boss/azhdaha/bg/cancel_l
function rlk:boss/azhdaha/bg/cancel_t
function rlk:boss/azhdaha/b3/special_cancel
function rlk:boss/azhdaha/fld/clear
kill @e[tag=rlk_mb_az_orb]
kill @e[tag=rlk_mb_az_orbc]
function rlk:boss/azhdaha/aft/clear
function rlk:boss/azhdaha/fx/tele/clear
function rlk:boss/azhdaha/svc/cine_off
function rlk:boss/azhdaha/rig/glow/gold_off
scoreboard players set #azTr mb 0
scoreboard players set #azTrN mb 0
scoreboard players set #azBur mb 0
scoreboard players set #azOrbHigh mb 0
scoreboard players set #azLastHit mb 0
scoreboard players set #mbNoLeash mb 0
scoreboard players set #azCastFirst mb 0
execute if score #azPh mb matches 1 run function rlk:boss/azhdaha/svc/floor_f1
execute if score #azPh mb matches 2 run function rlk:boss/azhdaha/svc/floor_f2
execute if score #azPh mb matches 3 run function rlk:boss/azhdaha/svc/floor_0
function rlk:boss/azhdaha/px/normal
function rlk:boss/azhdaha/rig/play/idle
scoreboard players set #azCool mb 10
scoreboard players set #azHudQ mb 1
