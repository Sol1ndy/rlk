# The idle clip of the current form / weapon (play: applied by the next rig/tick).
execute if score @s rdPhase matches 2 run return run function rlk:boss/raiden/rig/play/t_idle
execute if score @s rdWpn matches 1 run return run function rlk:boss/raiden/rig/play/idle_polearm
function rlk:boss/raiden/rig/play/idle_sword
