# Q0 stage hover: tick 0 (@s = body), clip q0_hover.
scoreboard players set #q0_s kn 1
scoreboard players set #q0_c kn 0
function rlk:boss/arlecchino/rig/play/q0_hover
function rlk:boss/arlecchino/p/q0/f/spot
function rlk:mboss/mv/face
function rlk:boss/arlecchino/rig/look/glow/crimson
execute at @s run function rlk:boss/arlecchino/fx/snd/apex
