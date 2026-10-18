# S6 section 3 (every 6 t while the wings are Pyro): rim embers at the forewing tips (idle-b rest anchors).
execute rotated as @s rotated ~ 0 positioned ^3.13 ^5.99 ^-1.33 run particle minecraft:small_flame ~ ~ ~ 0.15 0.15 0.15 0.005 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-3.13 ^5.99 ^-1.33 run particle minecraft:small_flame ~ ~ ~ 0.15 0.15 0.15 0.005 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^3.13 ^5.99 ^-1.33 run particle minecraft:dust{color:[0.886f,0.431f,0.314f],scale:0.6} ~ ~ ~ 0.1 0.1 0.1 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-3.13 ^5.99 ^-1.33 run particle minecraft:dust{color:[0.886f,0.431f,0.314f],scale:0.6} ~ ~ ~ 0.1 0.1 0.1 0 1 force @a[tag=player]
