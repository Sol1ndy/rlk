# A8 pattern tick 20.
function rlk:mboss/mv/face
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.95 ~ run function rlk:boss/scarlet/fx/p/ghost_trail {len:125}
function rlk:boss/scarlet/g/spot/side
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run function rlk:mboss/mv/glide {t:4}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
execute at @s run function rlk:boss/scarlet/fx/snd/g_dash
function rlk:boss/scarlet/g/cut/lock {s:27}
