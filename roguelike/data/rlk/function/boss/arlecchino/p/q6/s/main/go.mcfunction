# Q6 stage main: tick 0 (@s = body), clip q6.
scoreboard players set #q6_s kn 1
scoreboard players set #q6_c kn 0
function rlk:boss/arlecchino/rig/play/q6
function rlk:mboss/mv/face
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~0 213 ~-10 run function rlk:mboss/mv/glide {t:20}
execute at @s run function rlk:boss/arlecchino/fx/snd/leap
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.3 ~ run function rlk:boss/arlecchino/fx/p/leap_flare
