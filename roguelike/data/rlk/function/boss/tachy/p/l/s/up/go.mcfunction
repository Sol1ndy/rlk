# L stage up: tick 0 (@s = body).
scoreboard players set #l_s tk 1
scoreboard players set #l_c tk 0
function rlk:mboss/mv/face
function rlk:boss/tachy/rig/play/leap_high
execute at @s run function rlk:boss/tachy/fx/snd/leap
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.75 ~ run function rlk:boss/tachy/fx/p/wing_flare
execute at @s positioned ~ ~0.1 ~ run function rlk:boss/tachy/fx/p/dust_ring {r:20}
