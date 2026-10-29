# K stage lp: tick 0 (@s = body).
scoreboard players set #k_s tk 4
scoreboard players set #k_c tk 0
function rlk:boss/tachy/rig/play/k_leap
execute at @s run function rlk:boss/tachy/fx/snd/leap
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~ run function rlk:boss/tachy/fx/p/wing_flare
