# S2 transformation fx, clock 24 (@s = body, at it; the core's p/transform calls it).
execute rotated as @s rotated ~ 0 positioned ^3.13 ^5.99 ^-1.33 run particle minecraft:dust{color:[0.898f,0.984f,0.784f],scale:0.8} ~ ~ ~ 0.3 0.2 0.3 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-3.13 ^5.99 ^-1.33 run particle minecraft:dust{color:[0.898f,0.984f,0.784f],scale:0.8} ~ ~ ~ 0.3 0.2 0.3 0 2 force @a[tag=player]
function rlk:mboss/butterfly/fx/snd/flap_small
