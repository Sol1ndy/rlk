# jump clock 38
function rlk:mboss/butterfly/rig/face/track
particle minecraft:dust{color:[0.667f,0.859f,0.518f],scale:1} ~-1.32 ~2.05 ~-0.48 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.667f,0.859f,0.518f],scale:1} ~1.32 ~2.05 ~0.48 0 0 0 0 1 force @a[tag=player]
playsound minecraft:entity.breeze.idle_air hostile @a[tag=player] ~ ~ ~ 0.4 0.8 0.13
