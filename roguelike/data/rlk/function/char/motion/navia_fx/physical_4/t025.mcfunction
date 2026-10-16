# (retimed from t027)
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.45} ^0.3 ^3.1 ^-0.47 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.45} ^-0.65 ^3.33 ^0.46 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.55} ^0 ^0.42 ^0 0.25 0.25 0.25 0 2 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.5} ^0 ^2.76 ^0 1.3 1.3 1.3 0 3 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.35 ^3.31 ^-0.21 0.6 0.15 0.6 0 2 normal
function rlk:fx/nv/card {kind:"petal",pos:"^-1.1 ^2 ^-0.3",rot:"~ ~",bb:"center",roll:-60,spin:140,s0:0.14,s1:0.1,move:"0f,-0.7f,0f",life:22,fade:6}
