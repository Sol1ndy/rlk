# kick clock 20
execute store result score #bp1S mb run random value 0..1
execute at @s rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.898f,0.984f,0.784f],scale:0.7} ^-0.5 ^0.15 ^0.2 0.1 0.1 0.1 0 2 force @a[tag=player]
