# sweep clock 21
execute rotated as @s rotated ~ 0 positioned ^2.75 ^2.98 ^-0.56 run particle minecraft:dust{color:[0.973f,0.561f,0.224f],scale:1.2} ~ ~ ~ 0.1 0.1 0.1 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-2.75 ^2.98 ^-0.56 run particle minecraft:dust{color:[0.973f,0.561f,0.224f],scale:1.2} ~ ~ ~ 0.1 0.1 0.1 0 2 force @a[tag=player]
function rlk:mboss/butterfly/fx/snd/wing_dive
