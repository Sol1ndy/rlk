# A10 pattern tick 20
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run function rlk:mboss/mv/glide {t:2}
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ 203 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.6 2 0.6 0 20 force @a[tag=player]
execute at @s run playsound minecraft:entity.phantom.swoop hostile @a[tag=player] ~ ~ ~ 0.6 1.2 0.2
