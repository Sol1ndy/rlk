# Q5A stage main: tick 0 (@s = body), clip q5a.
scoreboard players set #q5a_s kn 1
scoreboard players set #q5a_c kn 0
function rlk:boss/arlecchino/rig/play/q5a
function rlk:mboss/mv/face
function rlk:boss/arlecchino/rig/look/glow/crimson
execute at @s run function rlk:boss/arlecchino/fx/snd/brand
