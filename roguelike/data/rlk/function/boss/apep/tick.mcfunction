# Hook tick (@s = body, at it, fight state #mbSt 1). Order (ap_contract 1.2): clocks, the hit flash, the floor
# events, the phase-2 stage (revival), the idle AI / decision (phases 1 and 3, not in a cine), the main slot,
# the yaw driver, the push request, the HUD, the rig tick, then the px-set driver (after the rig tick).
scoreboard players add #apFc mb 1
execute if score #apFlash mb matches 0.. run function rlk:boss/apep/u/flash
scoreboard players set #apFlash mb -1
execute if score #apPh mb matches 1 run function rlk:boss/apep/ev/tick
execute if score #apPh mb matches 1 run function rlk:boss/apep/ai/ring
execute if score #apPh mb matches 2 run function rlk:boss/apep/rev/tick
execute if score #apPid mb matches 0 unless score #mbCine mb matches 1 if score #apPh mb matches 1 run function rlk:boss/apep/ai/state
execute if score #apPid mb matches 0 unless score #mbCine mb matches 1 if score #apPh mb matches 3 run function rlk:boss/apep/ai/state
execute if score #apPid mb matches 1.. run function rlk:boss/apep/p/run
execute if score #apYawC mb matches 1.. run function rlk:boss/apep/yaw/tick
function rlk:boss/apep/push/req
function rlk:boss/apep/hud/tick
function rlk:boss/apep/rig/tick
function rlk:boss/apep/pxs/tick
scoreboard players set #apNoPush mb 0
