# strike clock 9
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p11a,limit=1] run function rlk:mboss/mv/glide {t:6}
playsound minecraft:entity.phantom.swoop hostile @a[tag=player] ~ ~ ~ 0.6 1.3 0.2
