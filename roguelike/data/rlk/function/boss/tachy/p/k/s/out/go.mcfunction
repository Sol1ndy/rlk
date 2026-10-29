# K stage out: tick 0 (@s = body).
scoreboard players set #k_s tk 1
scoreboard players set #k_c tk 0
function rlk:mboss/mv/face
function rlk:boss/tachy/rig/play/blink_out
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/tachy/fx/p/blink_out
execute at @s run function rlk:boss/tachy/fx/snd/blink_out
