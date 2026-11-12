# kick clock 17
playsound minecraft:block.moss.fall hostile @a[tag=player] ~ ~ ~ 0.35 1.2 0.12
execute store result score #bp1S mb run random value 0..1
execute at @s rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.898f,0.984f,0.784f],scale:0.7} ^-0.55 ^0.001 ^-0.719 0.1 0.1 0.1 0 2 force @a[tag=player]
