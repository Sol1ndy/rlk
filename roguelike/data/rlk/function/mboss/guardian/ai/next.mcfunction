# Next action. Test request > test lock (#mbLock 1-5 = that pattern only, 6 = guard pair + chaos only) >
# rotation: #gdLeft normal patterns, then guard I, guard II, chaos (K3).
execute if score #gdMv mb matches 1 run function rlk:mboss/guardian/rig/play/idle
scoreboard players set #gdMv mb 0
execute if score #gdReq mb matches 1.. run return run function rlk:mboss/guardian/ai/req
execute if score #mbLock mb matches 1..5 run return run function rlk:mboss/guardian/ai/lock
execute if score #mbLock mb matches 6 run return run function rlk:mboss/guardian/guard/begin1
execute if score #gdLeft mb matches ..0 run return run function rlk:mboss/guardian/guard/begin1
scoreboard players remove #gdLeft mb 1
function rlk:mboss/guardian/ai/pick
