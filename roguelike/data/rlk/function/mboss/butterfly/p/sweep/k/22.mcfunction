# sweep clock 22
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p13a,limit=1] run function rlk:mboss/mv/glide {t:4}
playsound minecraft:entity.phantom.swoop hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23
