# Q2 stage main: tick 0 (@s = body), clip q2.
scoreboard players set #q2_s kn 1
scoreboard players set #q2_c kn 0
function rlk:boss/arlecchino/rig/play/q2
function rlk:mboss/mv/face
execute at @s run function rlk:boss/arlecchino/fx/snd/wheel_spin
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~ run function rlk:boss/arlecchino/fx/p/embers_puff
