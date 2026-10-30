# K stage gl: tick 0 (@s = body).
scoreboard players set #k_s tk 3
scoreboard players set #k_c tk 0
function rlk:mboss/mv/face
function rlk:boss/tachy/rig/play/k_glint
function rlk:boss/tachy/rig/look/edge/glint
execute at @s rotated as @s rotated ~ 0 positioned ^-0.5 ^2 ^1.75 run function rlk:boss/tachy/fx/p/glint
execute at @s run function rlk:boss/tachy/fx/snd/glint
