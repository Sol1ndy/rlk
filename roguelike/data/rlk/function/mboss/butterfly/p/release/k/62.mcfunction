# release clock 62
function rlk:mboss/butterfly/rig/face/track
# amber ember petals and lime motes drift down
execute rotated as @s rotated ~ 0 positioned ^0 ^4.956 ^0.161 run function rlk:mboss/butterfly/fx/p/embers
execute rotated as @s rotated ~ 0 positioned ^0 ^4.956 ^0.161 run particle minecraft:dust{color:[0.769f,0.973f,0.494f],scale:0.8} ~ ~ ~ 1.5 1 1.5 0 2 force @a[tag=player]
