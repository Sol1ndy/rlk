# javelin clip tick 16
function rlk:mboss/guardian/rig/face/track
execute at @s rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"ring",pos:"^-0.9 ^1.5 ^1.2",rot:"~ ~",bb:"center",roll:0,spin:-170,s0:1,s1:0.6,move:"0f,0f,0f",life:4,fade:2}
execute at @s rotated as @s rotated ~ 0 positioned ^-0.9 ^1.5 ^1.2 run particle minecraft:dust{color:[0.969f,0.918f,0.663f],scale:0.55} ~ ~ ~ 0.35 0.35 0.35 0 3 force @a[tag=player]
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.5 1.8 0.17
