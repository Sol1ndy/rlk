# Q0 stage dive: tick 0 (@s = body), clip q0_dive.
scoreboard players set #q0_s kn 2
scoreboard players set #q0_c kn 0
function rlk:boss/arlecchino/rig/play/q0_dive
function rlk:boss/arlecchino/core/lockp
function rlk:boss/arlecchino/core/lock_short
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute positioned as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run function rlk:mboss/mv/glide {t:20}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run function rlk:boss/arlecchino/fx/p/dive_streak {len:100}
execute at @s run function rlk:boss/arlecchino/fx/snd/fall_dive
