# Q4 stage up: tick 0 (@s = body), clip q4_up.
scoreboard players set #q4_s kn 1
scoreboard players set #q4_c kn 0
function rlk:boss/arlecchino/rig/play/q4_up
function rlk:mboss/mv/face
function rlk:boss/arlecchino/p/q4/f/spot
execute at @s run function rlk:boss/arlecchino/fx/snd/leap
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.3 ~ run function rlk:boss/arlecchino/fx/p/leap_flare
