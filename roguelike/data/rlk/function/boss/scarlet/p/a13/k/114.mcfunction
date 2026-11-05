# A13 pattern tick 114.
function rlk:boss/scarlet/rig_stub/play/g_x
function rlk:boss/scarlet/g/spot/side
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run function rlk:mboss/mv/glide {t:2}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
