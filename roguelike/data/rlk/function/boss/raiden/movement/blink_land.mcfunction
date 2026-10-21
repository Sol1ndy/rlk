# Invisible (blink_out gone at 4): relocate (core blink_relocate), then reappear there.
function rlk:boss/raiden/blink_relocate
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/rig/play/t_blink_in
execute unless score @s rdPhase matches 2 run function rlk:boss/raiden/rig/play/blink_in
execute at @s run function rlk:boss/raiden/fx/blink_in
