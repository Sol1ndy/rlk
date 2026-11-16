# W1 stage ch: tick 0 (@s = body).
scoreboard players set #w1_s tk 2
scoreboard players set #w1_c tk 0
function rlk:mboss/mv/face
function rlk:boss/tachy/rig/play/w1_wave
execute at @s run function rlk:boss/tachy/fx/snd/step
