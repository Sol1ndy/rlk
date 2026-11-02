# C1 pattern tick 48
execute positioned as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run function rlk:mboss/mv/glide {t:6}
execute at @s run playsound minecraft:entity.phantom.swoop hostile @a[tag=player] ~ ~ ~ 0.8 1.2 0.27
