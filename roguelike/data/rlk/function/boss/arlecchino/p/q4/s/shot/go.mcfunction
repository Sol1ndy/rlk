# Q4 stage shot: tick 0 (@s = body), clip q4_shot.
scoreboard players set #q4_s kn 2
scoreboard players set #q4_c kn 0
function rlk:boss/arlecchino/rig/play/q4_shot
scoreboard players add #q4_k kn 1
function rlk:boss/arlecchino/rig/look/glow/crimson
execute at @s run function rlk:boss/arlecchino/fx/snd/beam_aim
function rlk:boss/arlecchino/p/q4/f/reticle
function rlk:boss/arlecchino/p/q4/f/aim
