# Play combo_end (20 t, clip id 20) from its tick 0 (@s = the body). The
# px sets of the clip follow it (pxs/tick reads the rig clock); the stance / looks / hands are the rig's.
function rlk:boss/apep/rig/play/combo_end
scoreboard players set #apYawC mb 0
scoreboard players set #apYawS mb 1
