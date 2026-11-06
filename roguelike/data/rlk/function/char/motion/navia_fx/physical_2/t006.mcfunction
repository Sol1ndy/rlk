# (retimed from t005)
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-2.1 ^0.25 ^-1.08 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1.88 ^0.4 ^-0.48 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-2.23 ^0.28 ^-0.74 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1.92 ^0.43 ^-0.18 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^-1.67 ^0.45 ^-0.54 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-2.32 ^0.31 ^-0.38 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1.92 ^0.46 ^0.12 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-2.36 ^0.35 ^-0.01 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1.88 ^0.5 ^0.41 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^-1.76 ^0.5 ^-0.01 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-2.35 ^0.39 ^0.36 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1.8 ^0.54 ^0.69 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-2.29 ^0.43 ^0.72 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1.7 ^0.58 ^0.96 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^-1.72 ^0.57 ^0.53 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-2.18 ^0.48 ^1.07 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1.56 ^0.62 ^1.21 0 0 0 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-1.92 ^0.46 ^0.12 0.08 0.08 0.08 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-1.7 ^0.58 ^0.96 0.08 0.08 0.08 0 1 normal
function rlk:fx/nv/card {kind:"crescent",pos:"^0 ^0.95 ^0",rot:"~ ~",bb:"fixed",roll:38,spin:45,s0:3.8,s1:4.4,move:"0f,0f,0f",life:9,fade:3}
