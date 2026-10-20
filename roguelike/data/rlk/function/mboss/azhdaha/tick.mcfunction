# Hook tick (@s = body, at it, fight state). Order (s2.md 3): clocks, the hit flash, brand + events, the floor
# queue, the zone sampler (every 4 t), the idle AI / decision, the main slot (patterns, services, the B3 frame),
# the cast slot, the bg slots L then T, the timers, the fields, the orbit centre, the push request, the HUD,
# the arena ambience, the yaw driver, the rig tick last.
scoreboard players add #azClk mb 1
execute if score #azFlash mb matches 1.. run function rlk:mboss/azhdaha/u/flash
scoreboard players set #azFlash mb 0
function rlk:mboss/azhdaha/brand/tick
function rlk:mboss/azhdaha/ev/tick
scoreboard players operation #azQ4 mb = #azClk mb
scoreboard players operation #azQ4 mb %= #azK4 mb
execute if score #azQ4 mb matches 0 run function rlk:mboss/azhdaha/ai/sample4
execute if score #azPat mb matches 0 run function rlk:mboss/azhdaha/ai/state
execute if score #azPat mb matches 1.. run function rlk:mboss/azhdaha/p/run
execute if score #azCast mb matches 1.. run function rlk:mboss/azhdaha/cast/run
execute if score #azBgL mb matches 1.. run function rlk:mboss/azhdaha/bg/run_l
execute if score #azBgT mb matches 1.. run function rlk:mboss/azhdaha/bg/run_t
scoreboard players set #azBgAny mb 0
execute if score #azBgL mb matches 1.. run scoreboard players set #azBgAny mb 1
execute if score #azBgT mb matches 1.. run scoreboard players set #azBgAny mb 1
execute if score #azAftN mb matches 1.. run function rlk:mboss/azhdaha/aft/tick
execute if score #azFldN mb matches 1.. run function rlk:mboss/azhdaha/fld/tick
execute if entity @e[type=minecraft:marker,tag=rlk_mb_az_orbc,limit=1] run function rlk:mboss/azhdaha/orb/centre
function rlk:mboss/azhdaha/push/req
function rlk:mboss/azhdaha/hud/tick
execute if score #azQ4 mb matches 0 run function rlk:mboss/azhdaha/arena/tick
execute if score #azYawC mb matches 1.. run function rlk:mboss/azhdaha/yaw/tick
function rlk:mboss/azhdaha/rig/tick
function rlk:mboss/azhdaha/rig_stub/chain
scoreboard players set #azNoPush mb 0
scoreboard players set #azNoTurn mb 0
