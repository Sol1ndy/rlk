particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.45} ^0.09 ^3.97 ^-1.51 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.45} ^0.04 ^4.03 ^0.31 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.55} ^0 ^0.96 ^-0.4 0.25 0.25 0.25 0 2 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.5} ^0 ^3.3 ^0 1.3 1.3 1.3 0 3 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.29 ^4.17 ^-0.62 0.6 0.15 0.6 0 2 normal
function rlk:fx/nv/card {kind:"petal",pos:"^0.7 ^2.8 ^1.1",rot:"~ ~",bb:"center",roll:40,spin:150,s0:0.15,s1:0.11,move:"0f,-0.9f,0f",life:26,fade:6}
function rlk:fx/nv/card {kind:"petal",pos:"^-0.7 ^2.5 ^-0.9",rot:"~ ~",bb:"center",roll:-30,spin:-140,s0:0.13,s1:0.1,move:"0f,-0.8f,0f",life:26,fade:6}
