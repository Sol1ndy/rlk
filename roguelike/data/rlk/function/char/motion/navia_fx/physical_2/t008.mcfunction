particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.76 ^2.47 ^0.78 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^1.31 ^2.45 ^0.3 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.69 ^2.64 ^0.6 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^1.2 ^2.58 ^0.17 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^1.21 ^2.27 ^0.47 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.6 ^2.81 ^0.42 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^1.07 ^2.71 ^0.05 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.49 ^2.97 ^0.26 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^0.93 ^2.83 ^-0.06 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^1.07 ^2.52 ^0.22 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.35 ^3.12 ^0.11 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^0.78 ^2.94 ^-0.15 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.2 ^3.27 ^-0.02 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^0.62 ^3.04 ^-0.22 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^0.86 ^2.75 ^0 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.02 ^3.4 ^-0.14 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^0.45 ^3.12 ^-0.28 0 0 0 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^1.07 ^2.71 ^0.05 0.08 0.08 0.08 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^0.62 ^3.04 ^-0.22 0.08 0.08 0.08 0 1 normal
function rlk:fx/nv/card {kind:"shard",pos:"^0.38 ^0 ^1.75",rot:"~-8 ~",bb:"fixed",roll:16,spin:0,s0:0,s1:1.3,move:"0f,0f,0f",life:7,fade:3}
function rlk:fx/nv/card {kind:"shard",pos:"^0.07 ^0 ^1.71",rot:"~12 ~",bb:"fixed",roll:-12,spin:0,s0:0,s1:1,move:"0f,0f,0f",life:7,fade:3}
function rlk:fx/nv/p/hit_ring {pos:"^0.2 ^1 ^1.96"}
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^0.12 ^0.7 ^1.53 0.35 0.45 0.35 0 8 normal
