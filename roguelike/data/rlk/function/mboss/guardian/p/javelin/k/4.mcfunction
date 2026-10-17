# javelin clip tick 4
function rlk:mboss/guardian/rig/face/track
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.23
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.3 1.5 0.1
execute at @s rotated as @s rotated ~ 0 positioned ^-2.859 ^2.397 ^0.916 run particle minecraft:dust{color:[0.992f,0.957f,0.584f],scale:1} ~ ~ ~ 0.04 0.04 0.04 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-2.83 ^2.463 ^0.905 run particle minecraft:dust{color:[0.992f,0.957f,0.584f],scale:1} ~ ~ ~ 0.04 0.04 0.04 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-2.802 ^2.53 ^0.895 run particle minecraft:dust{color:[0.992f,0.957f,0.584f],scale:1} ~ ~ ~ 0.04 0.04 0.04 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-2.773 ^2.597 ^0.885 run particle minecraft:dust{color:[1f,0.96f,0.75f],scale:1} ~ ~ ~ 0.04 0.04 0.04 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-1.482 ^2.571 ^0.756 run particle minecraft:dust{color:[0.78f,0.675f,0.341f],scale:0.7} ~ ~ ~ 0.05 0.05 0.05 0 1 force @a[tag=player]
