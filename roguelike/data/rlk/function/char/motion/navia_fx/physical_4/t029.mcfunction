particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.45} ^-1.27 ^3.44 ^-0.2 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.45} ^0.37 ^3.09 ^-0.9 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.55} ^0 ^0.13 ^-0.1 0.25 0.25 0.25 0 2 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.5} ^0 ^2.48 ^0 1.3 1.3 1.3 0 3 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.29 ^3.34 ^-0.2 0.6 0.15 0.6 0 2 normal
function rlk:fx/nv/card {kind:"petal",pos:"^0.4 ^1.7 ^0.8",rot:"~ ~",bb:"center",roll:20,spin:-150,s0:0.13,s1:0.1,move:"0f,-0.6f,0f",life:20,fade:6}
