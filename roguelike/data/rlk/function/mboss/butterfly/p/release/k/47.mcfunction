# release clock 47
function rlk:mboss/butterfly/rig/face/track
# she re-emerges: lime tendrils stream out
execute rotated as @s rotated ~ 0 positioned ^0 ^4.956 ^0.161 run function rlk:mboss/butterfly/fx/p/rel_tendrils
execute rotated as @s rotated ~ 0 positioned ^0 ^4.956 ^0.161 run particle minecraft:dust{color:[0.6f,0.89f,0.345f],scale:1.2} ~ ~ ~ 1.5 1 1.5 0 20 force @a[tag=player]
