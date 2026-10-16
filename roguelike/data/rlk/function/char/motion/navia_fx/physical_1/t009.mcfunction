particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-1.86 ^2.29 ^1.41 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1.23 ^2.1 ^1.46 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-1.66 ^2.28 ^1.62 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1.04 ^2.07 ^1.59 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^-1.27 ^2.01 ^1.22 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-1.44 ^2.25 ^1.82 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-0.83 ^2.03 ^1.71 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-1.2 ^2.2 ^1.99 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-0.62 ^1.98 ^1.8 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^-0.92 ^1.97 ^1.49 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-0.95 ^2.15 ^2.14 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-0.4 ^1.92 ^1.87 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-0.7 ^2.08 ^2.26 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-0.18 ^1.86 ^1.93 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^-0.55 ^1.9 ^1.69 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-0.43 ^2 ^2.36 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^0.04 ^1.79 ^1.96 0 0 0 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.83 ^2.03 ^1.71 0.08 0.08 0.08 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.18 ^1.86 ^1.93 0.08 0.08 0.08 0 1 normal
function rlk:fx/nv/card {kind:"burst",pos:"^-0.22 ^1.75 ^1.89",rot:"~ ~",bb:"center",roll:8,spin:14,s0:0.5,s1:1.9,move:"0f,0f,0f",life:5,fade:2}
function rlk:fx/nv/card {kind:"glow",pos:"^-0.22 ^1.75 ^2.04",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.6,s1:1.6,move:"0f,0f,0f",life:5,fade:2}
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.2} ^-0.22 ^1.75 ^1.89 0.35 0.35 0.35 0 10 normal
particle minecraft:end_rod ^-0.22 ^1.75 ^1.89 0.25 0.25 0.25 0.06 5 normal
execute if score @s nvP matches 1.. run function rlk:fx/nv/p/glint {pos:"^0.08 ^2 ^1.79"}
