particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^0.57 ^2.35 ^2.08 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^0.78 ^2.31 ^1.46 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^0.76 ^2.51 ^1.9 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^0.91 ^2.4 ^1.27 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^0.54 ^2.21 ^1.4 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^0.94 ^2.65 ^1.68 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^1.03 ^2.48 ^1.06 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.11 ^2.76 ^1.44 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^1.13 ^2.52 ^0.83 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^0.78 ^2.4 ^1.07 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.27 ^2.85 ^1.18 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^1.22 ^2.55 ^0.6 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.4 ^2.91 ^0.9 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^1.29 ^2.56 ^0.36 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^0.98 ^2.51 ^0.67 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.52 ^2.94 ^0.61 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^1.34 ^2.54 ^0.12 0 0 0 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^1.03 ^2.48 ^1.06 0.08 0.08 0.08 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^1.29 ^2.56 ^0.36 0.08 0.08 0.08 0 1 normal
function rlk:fx/nv/card {kind:"crescent",pos:"^0 ^1.3 ^0",rot:"~-95 ~",bb:"fixed",roll:-38,spin:40,s0:4,s1:4.5,move:"0f,0f,0f",life:5,fade:2}
function rlk:fx/nv/p/hit_ring {pos:"^-0.22 ^1.7 ^1.94"}
