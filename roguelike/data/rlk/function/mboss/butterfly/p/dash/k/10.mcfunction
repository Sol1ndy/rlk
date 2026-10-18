# dash clock 10
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] run function rlk:mboss/mv/glide {t:2}
playsound minecraft:entity.breeze.jump hostile @a[tag=player] ~ ~ ~ 0.7 1.3 0.23
