# (retimed from t006)
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-1.93 ^0.49 ^1.39 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1.29 ^0.66 ^1.42 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-1.62 ^0.52 ^1.68 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-1 ^0.7 ^1.59 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^-1.23 ^0.64 ^1.22 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-1.28 ^0.56 ^1.93 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-0.69 ^0.76 ^1.72 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-0.9 ^0.62 ^2.12 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-0.37 ^0.82 ^1.8 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^-0.7 ^0.72 ^1.54 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-0.51 ^0.69 ^2.25 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^-0.04 ^0.9 ^1.84 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^-0.11 ^0.78 ^2.32 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^0.27 ^0.98 ^1.83 0 0 0 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.75} ^-0.13 ^0.84 ^1.71 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.05} ^0.29 ^0.87 ^2.33 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.95} ^0.57 ^1.06 ^1.77 0 0 0 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.69 ^0.76 ^1.72 0.08 0.08 0.08 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^0.27 ^0.98 ^1.83 0.08 0.08 0.08 0 1 normal
function rlk:fx/nv/card {kind:"burst",pos:"^0.2 ^0.95 ^1.91",rot:"~ ~",bb:"center",roll:-10,spin:16,s0:0.45,s1:1.6,move:"0f,0f,0f",life:5,fade:2}
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.1} ^0.2 ^0.95 ^1.91 0.3 0.3 0.3 0 8 normal
particle minecraft:end_rod ^0.2 ^0.95 ^1.91 0.2 0.2 0.2 0.05 4 normal
execute if score @s nvP matches 1.. run function rlk:fx/nv/p/glint {pos:"^-0.05 ^1.25 ^1.81"}
