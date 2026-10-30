# (retimed from t011)
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^0.5 ^2.27 ^2.17 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^0.71 ^2.24 ^1.55 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^0.69 ^2.44 ^2.01 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^0.84 ^2.33 ^1.38 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^0.47 ^2.14 ^1.52 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^0.87 ^2.58 ^1.82 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^0.96 ^2.4 ^1.2 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.04 ^2.69 ^1.61 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^1.06 ^2.46 ^1 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^0.71 ^2.33 ^1.24 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.2 ^2.78 ^1.38 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^1.15 ^2.49 ^0.79 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.33 ^2.85 ^1.12 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^1.21 ^2.5 ^0.58 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^0.91 ^2.45 ^0.9 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.44 ^2.88 ^0.86 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^1.26 ^2.48 ^0.37 0 0 0 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^0.96 ^2.4 ^1.2 0.08 0.08 0.08 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^1.21 ^2.5 ^0.58 0.08 0.08 0.08 0 1 normal
function rlk:fx/nv/card {kind:"crescent",pos:"^0 ^1.3 ^0",rot:"~-95 ~",bb:"fixed",roll:-38,spin:40,s0:4,s1:4.5,move:"0f,0f,0f",life:8,fade:3}
function rlk:fx/nv/p/hit_ring {pos:"^-0.24 ^1.7 ^1.95"}
