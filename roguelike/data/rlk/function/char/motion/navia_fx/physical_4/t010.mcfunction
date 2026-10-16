function rlk:fx/nv/card {kind:"star",pos:"^-0.21 ^1.15 ^1.62",rot:"~ ~",bb:"center",roll:0,spin:40,s0:0.2,s1:0.9,move:"0f,0f,0f",life:4,fade:2}
function rlk:fx/nv/card {kind:"glow",pos:"^-0.1 ^1.3 ^2.9",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.6,s1:1.6,move:"0f,0f,0f",life:6,fade:3}
function rlk:fx/nv/card {kind:"burst",pos:"^-0.1 ^1.28 ^2.59",rot:"~ ~",bb:"center",roll:12,spin:18,s0:0.6,s1:2.5,move:"0f,0f,0f",life:5,fade:2}
particle minecraft:flash{color:[1.0,0.95,0.77,1.0]} ^-0.1 ^1.3 ^2.7 0 0 0 0 1 normal
particle minecraft:end_rod ^-0.1 ^1.3 ^2.7 0.1 0.1 0.1 0.18 8 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:1.1} ^-0.1 ^1.3 ^2.7 0.35 0.35 0.35 0 10 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.8} ^-0.1 ^1.3 ^2.7 0.15 0.15 0.15 0 6 normal
particle minecraft:end_rod ^-0.21 ^1.15 ^1.62 0.04 0.04 0.04 0.06 3 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.7} ^-0.21 ^1.15 ^1.62 0.05 0.05 0.05 0 4 normal
execute if score @s nvP matches 1.. run function rlk:fx/nv/card {kind:"star",pos:"^-0.1 ^1.55 ^2.7",rot:"~ ~",bb:"center",roll:0,spin:-40,s0:0.3,s1:1.1,move:"0f,0f,0f",life:5,fade:2}
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.1 ^1.3 ^2.7 0.5 0.5 0.5 0 10 normal
execute if score @s nvP matches 1.. run particle minecraft:dust{color:[0.914,0.725,0.286],scale:1.2} ^-0.1 ^1.3 ^2.7 0.45 0.45 0.45 0 8 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.4} ^-0.21 ^1.15 ^1.62 0.01 0.01 0.01 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.4} ^-0.2 ^1.17 ^1.74 0.01 0.01 0.01 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.4} ^-0.19 ^1.19 ^1.86 0.01 0.01 0.01 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.4} ^-0.17 ^1.2 ^1.98 0.01 0.01 0.01 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.4} ^-0.16 ^1.22 ^2.11 0.01 0.01 0.01 0 1 normal
