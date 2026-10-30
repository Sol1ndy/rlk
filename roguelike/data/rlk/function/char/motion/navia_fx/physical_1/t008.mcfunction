# (retimed from t008)
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-2.58 ^1.34 ^-0.44 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-2.16 ^1.47 ^0.04 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-2.57 ^1.52 ^-0.17 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-2.09 ^1.61 ^0.27 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^-1.96 ^1.42 ^-0.11 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-2.53 ^1.7 ^0.11 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-2 ^1.73 ^0.5 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-2.45 ^1.87 ^0.39 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1.88 ^1.85 ^0.71 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^-1.87 ^1.68 ^0.31 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-2.34 ^2.03 ^0.66 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1.75 ^1.95 ^0.92 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-2.21 ^2.17 ^0.93 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1.59 ^2.05 ^1.12 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^-1.69 ^1.91 ^0.72 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-2.04 ^2.3 ^1.18 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1.42 ^2.12 ^1.31 0 0 0 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-2 ^1.73 ^0.5 0.08 0.08 0.08 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-1.59 ^2.05 ^1.12 0.08 0.08 0.08 0 1 normal
function rlk:fx/nv/card {kind:"crescent",pos:"^0 ^1.4 ^0",rot:"~ ~",bb:"fixed",roll:22,spin:45,s0:4,s1:4.6,move:"0f,0f,0f",life:9,fade:3}
