# kick clock 0
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p1a,limit=1] run function rlk:mboss/mv/glide {t:5}
playsound minecraft:entity.breeze.jump hostile @a[tag=player] ~ ~ ~ 0.6 1.3 0.2
