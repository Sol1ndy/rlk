# The rig was respawned during the balance groggy (@s = body; the reload hook): down (loop) at once while more than
# 20 t are left, else kipup from the tick it has reached (its clock hrRigT = 20 - grgT; the next rig/tick shows
# the following tick).
execute if score @s grgT matches 21.. run return run function rlk:boss/scarlet/rig/play/down
scoreboard players set #t hr 20
scoreboard players operation #t hr -= @s grgT
function rlk:boss/scarlet/rig/play/kipup
scoreboard players operation @s hrRigT = #t hr
