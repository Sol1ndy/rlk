# A13 pattern tick 131.
function rlk:boss/scarlet/g/spot/far
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run function rlk:mboss/mv/glide {t:10}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
