# A13 deflect (T + 2 after the judge; @s = the body): from 1 b above the player down to the blade lock
# 1.2 b in front of them in 8 t (g_deflect fall -> lock), facing them.
function rlk:mboss/mv/face
function rlk:boss/scarlet/g/spot/lock
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run function rlk:mboss/mv/glide {t:8}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
