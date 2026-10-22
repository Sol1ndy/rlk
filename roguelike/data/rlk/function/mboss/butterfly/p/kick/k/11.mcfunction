# kick clock 11
function rlk:mboss/mv/away {d:0.15}
execute at @s rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.757f,0.969f,0.533f],scale:1} ^0 ^2.756 ^-0.445 0.15 0.2 0.15 0 2 force @a[tag=player]
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.3 1.6 0.1
