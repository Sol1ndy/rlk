# jump clock 36
function rlk:mboss/butterfly/rig/face/track
particle minecraft:dust{color:[0.667f,0.859f,0.518f],scale:1} ~0.7 ~1.35 ~-1.21 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.667f,0.859f,0.518f],scale:1} ~-0.7 ~1.35 ~1.21 0 0 0 0 1 force @a[tag=player]
playsound minecraft:item.elytra.flying hostile @a[tag=player] ~ ~ ~ 0.2 1.4 0
