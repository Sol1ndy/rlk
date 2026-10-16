particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.45} ^-1 ^4 ^0.08 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.45} ^-0.26 ^3.78 ^-1.57 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.55} ^0 ^0.72 ^-0.31 0.25 0.25 0.25 0 2 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.5} ^0 ^3.06 ^0 1.3 1.3 1.3 0 3 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.28 ^3.92 ^-0.59 0.6 0.15 0.6 0 2 normal
function rlk:fx/nv/card {kind:"petal",pos:"^1.1 ^2.3 ^0.4",rot:"~ ~",bb:"center",roll:70,spin:150,s0:0.15,s1:0.11,move:"0f,-0.8f,0f",life:24,fade:6}
function rlk:fx/nv/p/glint {pos:"^-1 ^4 ^0.08"}
