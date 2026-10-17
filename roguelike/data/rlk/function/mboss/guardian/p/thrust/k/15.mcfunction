# thrust clip tick 15
function rlk:mboss/guardian/rig/face/track
execute at @s rotated as @s rotated ~ 0 positioned ^-1.232 ^2.643 ^0.036 run particle minecraft:dust_color_transition{from_color:[0.804f,0.702f,0.494f],to_color:[0.616f,0.525f,0.314f],scale:0.9} ~ ~ ~ 0.03 0.03 0.03 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-2.043 ^2.738 ^0.314 run particle minecraft:dust_color_transition{from_color:[0.988f,0.961f,0.682f],to_color:[0.616f,0.525f,0.314f],scale:0.9} ~ ~ ~ 0.03 0.03 0.03 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-2.901 ^2.655 ^0.44 run particle minecraft:dust_color_transition{from_color:[0.804f,0.702f,0.494f],to_color:[0.616f,0.525f,0.314f],scale:0.9} ~ ~ ~ 0.03 0.03 0.03 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-3.639 ^2.715 ^0.654 run particle minecraft:dust_color_transition{from_color:[0.988f,0.961f,0.682f],to_color:[0.616f,0.525f,0.314f],scale:0.9} ~ ~ ~ 0.03 0.03 0.03 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-4.413 ^2.823 ^0.94 run particle minecraft:dust_color_transition{from_color:[0.804f,0.702f,0.494f],to_color:[0.616f,0.525f,0.314f],scale:0.9} ~ ~ ~ 0.03 0.03 0.03 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-5.23 ^2.789 ^1.218 run particle minecraft:dust_color_transition{from_color:[0.988f,0.961f,0.682f],to_color:[0.616f,0.525f,0.314f],scale:0.9} ~ ~ ~ 0.03 0.03 0.03 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-3.935 ^2.777 ^0.79 run particle minecraft:dust{color:[1f,0.96f,0.75f],scale:0.5} ~ ~ ~ 0.12 0.12 0.12 0 2 force @a[tag=player]
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.6 1.9 0.3
playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.25 2 0.3
