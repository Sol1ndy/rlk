# W1 stage bl: tick 0 (@s = body).
scoreboard players set #w1_s tk 1
scoreboard players set #w1_c tk 0
function rlk:mboss/mv/face
function rlk:boss/tachy/rig/play/backstep
execute at @s run function rlk:boss/tachy/fx/snd/step
execute at @s rotated as @s rotated ~180 0 positioned ^ ^ ^1.5 if function rlk:mboss/mv/ok run function rlk:mboss/mv/glide {t:10}
