# R2 pattern tick 4.
function rlk:boss/scarlet/g/spot/back
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run function rlk:mboss/mv/glide {t:10}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
