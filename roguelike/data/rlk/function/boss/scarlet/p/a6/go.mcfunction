# A6: glide to the probe point in 3 t (the probe never leaves mv/ok ground).
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_dp,limit=1] run function rlk:mboss/mv/glide {t:3}
kill @e[type=minecraft:marker,tag=rlk_hr_dp]
