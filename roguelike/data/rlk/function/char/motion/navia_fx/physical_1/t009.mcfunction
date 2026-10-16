particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-1.86 ^2.28 ^1.41 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1.24 ^2.09 ^1.46 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-1.67 ^2.26 ^1.63 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1.05 ^2.05 ^1.59 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^-1.28 ^1.99 ^1.23 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-1.45 ^2.22 ^1.82 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-0.85 ^2 ^1.71 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-1.22 ^2.16 ^2 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-0.64 ^1.94 ^1.81 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^-0.95 ^1.93 ^1.5 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-0.98 ^2.1 ^2.15 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-0.43 ^1.87 ^1.88 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-0.73 ^2.02 ^2.27 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-0.21 ^1.8 ^1.94 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^-0.58 ^1.84 ^1.7 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-0.47 ^1.93 ^2.37 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^0 ^1.72 ^1.97 0 0 0 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.85 ^2 ^1.71 0.08 0.08 0.08 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.21 ^1.8 ^1.94 0.08 0.08 0.08 0 1 normal
function rlk:fx/nv/card {kind:"burst",pos:"^-0.24 ^1.75 ^1.9",rot:"~ ~",bb:"center",roll:8,spin:14,s0:0.5,s1:1.9,move:"0f,0f,0f",life:5,fade:2}
function rlk:fx/nv/card {kind:"glow",pos:"^-0.24 ^1.75 ^2.05",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.6,s1:1.6,move:"0f,0f,0f",life:5,fade:2}
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.2} ^-0.24 ^1.75 ^1.9 0.35 0.35 0.35 0 10 normal
particle minecraft:end_rod ^-0.24 ^1.75 ^1.9 0.25 0.25 0.25 0.06 5 normal
execute if score @s nvP matches 1.. run function rlk:fx/nv/p/glint {pos:"^0.06 ^2 ^1.8"}
