# Q1 stage main: tick 0 (@s = body), clip q1.
scoreboard players set #q1_s kn 1
scoreboard players set #q1_c kn 0
function rlk:boss/arlecchino/rig/play/q1
function rlk:mboss/mv/face
execute at @s run function rlk:boss/arlecchino/fx/snd/step
function rlk:boss/arlecchino/p/q1/f/lunge
