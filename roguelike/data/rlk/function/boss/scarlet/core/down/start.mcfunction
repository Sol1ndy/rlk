# The down window after CS2 (@s = body): 200 t on her back (clip down), normal damage, the under bar = the ticks
# left (gold); at its end the kipup (20 t, invulnerable) -> P2 after 12 t; a hit reaching the
# 5 % floor -> lead_down 40 t later.
scoreboard players set #ph hr 6
scoreboard players set #sqn hr 0
scoreboard players set #inv hr 0
scoreboard players set #down hr 200
scoreboard players set #flw hr 0
scoreboard players set #kip hr 0
scoreboard players set #fl hr 0
function rlk:boss/scarlet/rig/play/down
# balance gauge (combat overhaul lane B): the down window refills it (a pending balance groggy is dropped)
function rlk:bal/refill
