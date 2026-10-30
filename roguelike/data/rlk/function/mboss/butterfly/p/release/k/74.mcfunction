# release clock 74
function rlk:mboss/butterfly/rig/face/track
execute rotated as @s rotated ~ 0 positioned ^2.858 ^6.793 ^-1.227 run particle minecraft:dust{color:[0.906f,0.992f,0.478f],scale:1} ~ ~ ~ 0.2 0.2 0.2 0 6 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-2.858 ^6.793 ^-1.227 run particle minecraft:dust{color:[0.906f,0.992f,0.478f],scale:1} ~ ~ ~ 0.2 0.2 0.2 0 6 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^2.513 ^4.059 ^-0.538 run particle minecraft:dust{color:[0.906f,0.992f,0.478f],scale:1} ~ ~ ~ 0.2 0.2 0.2 0 6 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-2.513 ^4.059 ^-0.538 run particle minecraft:dust{color:[0.906f,0.992f,0.478f],scale:1} ~ ~ ~ 0.2 0.2 0.2 0 6 force @a[tag=player]
playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ 0.6 1.8 0.2
