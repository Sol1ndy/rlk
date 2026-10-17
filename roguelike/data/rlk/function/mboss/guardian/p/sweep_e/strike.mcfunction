# Element-coloured strike fx over the arc (#gdSwEl), every tick of the active window.
execute if score #gdSwEl mb matches 1 rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.541f,0.298f],scale:1.5} ^ ^0.8 ^3.0 2.6 0.4 1.6 0 10 force @a[tag=player]
execute if score #gdSwEl mb matches 1 rotated as @s rotated ~ 0 run particle minecraft:flame ^ ^0.8 ^3.0 2.4 0.4 1.4 0.03 8 force @a[tag=player]
execute if score #gdSwEl mb matches 2 rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.361f,0.784f,1f],scale:1.5} ^ ^0.8 ^3.0 2.6 0.4 1.6 0 10 force @a[tag=player]
execute if score #gdSwEl mb matches 2 rotated as @s rotated ~ 0 run particle minecraft:splash ^ ^0.8 ^3.0 2.4 0.4 1.4 0.2 8 force @a[tag=player]
execute if score #gdSwEl mb matches 3 rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.894f,0.518f,0.988f],scale:1.5} ^ ^0.8 ^3.0 2.6 0.4 1.6 0 10 force @a[tag=player]
execute if score #gdSwEl mb matches 3 rotated as @s rotated ~ 0 run particle minecraft:electric_spark ^ ^0.8 ^3.0 2.4 0.4 1.4 0.2 8 force @a[tag=player]
execute if score #gdSwEl mb matches 4 rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.635f,0.996f,0.992f],scale:1.5} ^ ^0.8 ^3.0 2.6 0.4 1.6 0 10 force @a[tag=player]
execute if score #gdSwEl mb matches 4 rotated as @s rotated ~ 0 run particle minecraft:snowflake ^ ^0.8 ^3.0 2.4 0.4 1.4 0.05 8 force @a[tag=player]
