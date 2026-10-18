# sweep clock 20
execute rotated as @s rotated ~ 0 positioned ^2.302 ^5.027 ^-1.389 run particle minecraft:dust{color:[0.973f,0.561f,0.224f],scale:1.2} ~ ~ ~ 0.1 0.1 0.1 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-2.302 ^5.027 ^-1.389 run particle minecraft:dust{color:[0.973f,0.561f,0.224f],scale:1.2} ~ ~ ~ 0.1 0.1 0.1 0 2 force @a[tag=player]
# the head-first dive: glide to P
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p13p,limit=1] run function rlk:mboss/mv/glide {t:6}
playsound minecraft:entity.phantom.swoop hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23
