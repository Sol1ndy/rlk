# javelin clip tick 11
function rlk:mboss/guardian/rig/face/track
execute at @s rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"star",pos:"^-0.9 ^1.5 ^1.2",rot:"~ ~",bb:"center",roll:0,spin:170,s0:1.6,s1:0.75,move:"0f,0f,0f",life:14,fade:2}
execute at @s rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"glow",pos:"^-0.9 ^1.5 ^1.2",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.6,s1:1.4,move:"0f,0f,0f",life:13,fade:4}
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.8 1.3 0.3
execute at @s rotated as @s rotated ~ 0 positioned ^-0.9 ^1.5 ^1.2 run particle minecraft:dust{color:[0.969f,0.918f,0.663f],scale:0.55} ~ ~ ~ 0.35 0.35 0.35 0 3 force @a[tag=player]
