# A8 pattern tick 33.
function rlk:boss/scarlet/g/cut/lock {s:40}
function rlk:mboss/mv/face
function rlk:boss/scarlet/g/spot/side
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run function rlk:mboss/mv/glide {t:3}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
