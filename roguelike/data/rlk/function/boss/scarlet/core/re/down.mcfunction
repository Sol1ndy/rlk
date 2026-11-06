# /reload in the down window: it goes on with at most 100 t left (the kipup: P2).
execute if score #kip hr matches 1.. run return run function rlk:boss/scarlet/core/p2/from_down
execute if score #down hr matches 101.. run scoreboard players set #down hr 100
function rlk:boss/scarlet/rig/play/down
