# Q5B stage main: tick 0 (@s = body), clip q5b.
scoreboard players set #q5b_s kn 1
scoreboard players set #q5b_c kn 0
function rlk:boss/arlecchino/rig/play/q5b
function rlk:mboss/mv/face
function rlk:boss/arlecchino/rig/look/glow/crimson
execute at @s run function rlk:boss/arlecchino/fx/snd/brand
