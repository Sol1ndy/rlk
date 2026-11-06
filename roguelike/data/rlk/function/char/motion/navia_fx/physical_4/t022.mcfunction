# (retimed from t022)
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.55} ^0.32 ^3.75 ^0 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.55} ^0.01 ^3.82 ^0.46 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.55} ^-0.52 ^3.93 ^0.56 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.55} ^-0.97 ^4.01 ^0.24 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.55} ^-1.07 ^4.02 ^-0.31 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.55} ^-0.76 ^3.96 ^-0.76 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.55} ^-0.22 ^3.85 ^-0.86 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.55} ^0.23 ^3.76 ^-0.55 0.03 0.03 0.03 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.36 ^3.96 ^-0.15 0.5 0.2 0.5 0 8 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.45} ^-1.07 ^4.02 ^-0.31 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.45} ^0.23 ^3.76 ^-0.55 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.55} ^0 ^1.07 ^0 0.25 0.25 0.25 0 2 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.5} ^0 ^3.4 ^0 1.3 1.3 1.3 0 3 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.36 ^3.96 ^-0.15 0.6 0.15 0.6 0 2 normal
# (retimed from t023)
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.45} ^-0.07 ^3.7 ^-0.87 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.45} ^-0.11 ^3.75 ^0.47 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.55} ^0 ^0.96 ^0 0.25 0.25 0.25 0 2 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.5} ^0 ^3.3 ^0 1.3 1.3 1.3 0 3 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.35 ^3.85 ^-0.21 0.6 0.15 0.6 0 2 normal
function rlk:fx/nv/card {kind:"petal",pos:"^0.7 ^2.8 ^1.1",rot:"~ ~",bb:"center",roll:40,spin:150,s0:0.15,s1:0.11,move:"0f,-0.9f,0f",life:26,fade:6}
function rlk:fx/nv/card {kind:"petal",pos:"^-0.7 ^2.5 ^-0.9",rot:"~ ~",bb:"center",roll:-30,spin:-140,s0:0.13,s1:0.1,move:"0f,-0.8f,0f",life:26,fade:6}
