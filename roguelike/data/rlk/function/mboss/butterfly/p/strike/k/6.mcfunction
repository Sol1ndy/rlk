# strike clock 6
function rlk:mboss/butterfly/wx/u/toward {d:0.15}
execute rotated as @s rotated ~ 0 positioned ^2.442 ^6.428 ^-1.424 run particle minecraft:dust{color:[0.906f,0.992f,0.667f],scale:0.8} ~ ~ ~ 0.2 0.2 0.2 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-2.442 ^6.428 ^-1.424 run particle minecraft:dust{color:[0.906f,0.992f,0.667f],scale:0.8} ~ ~ ~ 0.2 0.2 0.2 0 2 force @a[tag=player]
