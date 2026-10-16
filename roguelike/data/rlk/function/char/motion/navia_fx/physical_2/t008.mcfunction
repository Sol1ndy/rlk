particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.75 ^2.41 ^0.95 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^1.3 ^2.39 ^0.47 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.71 ^2.58 ^0.79 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^1.22 ^2.53 ^0.36 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^1.23 ^2.21 ^0.66 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.65 ^2.75 ^0.64 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^1.12 ^2.66 ^0.27 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.57 ^2.91 ^0.5 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^1.01 ^2.78 ^0.19 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^1.15 ^2.46 ^0.46 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.46 ^3.07 ^0.38 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^0.89 ^2.89 ^0.12 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.34 ^3.22 ^0.27 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^0.76 ^2.98 ^0.07 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^1 ^2.7 ^0.29 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^1.19 ^3.35 ^0.18 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^0.62 ^3.07 ^0.04 0 0 0 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^1.12 ^2.66 ^0.27 0.08 0.08 0.08 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^0.76 ^2.98 ^0.07 0.08 0.08 0.08 0 1 normal
function rlk:fx/nv/card {kind:"shard",pos:"^0.38 ^0 ^1.75",rot:"~-8 ~",bb:"fixed",roll:16,spin:0,s0:0,s1:1.3,move:"0f,0f,0f",life:7,fade:3}
function rlk:fx/nv/card {kind:"shard",pos:"^0.07 ^0 ^1.71",rot:"~12 ~",bb:"fixed",roll:-12,spin:0,s0:0,s1:1,move:"0f,0f,0f",life:7,fade:3}
function rlk:fx/nv/p/hit_ring {pos:"^0.2 ^1 ^1.96"}
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^0.12 ^0.7 ^1.53 0.35 0.45 0.35 0 8 normal
