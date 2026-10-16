# flourish (v1 K2): gold motes shed from the canopy rim
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.6} ^-0.824 ^1.763 ^0.312 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.6} ^-0.559 ^1.512 ^0.661 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.6} ^-0.651 ^1.056 ^0.857 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.6} ^-1.029 ^0.739 ^0.753 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.6} ^-1.409 ^0.8 ^0.427 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.6} ^-1.505 ^1.192 ^0.125 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.6} ^-1.245 ^1.621 ^0.074 0.03 0.03 0.03 0 1 normal
function rlk:fx/nv/card {kind:"star",pos:"^-1.366 ^0.803 ^0.458",rot:"~ ~",bb:"center",roll:0,spin:-45,s0:0.05,s1:0.42,move:"0f,0f,0f",life:5,fade:2}
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-1.032 ^1.24 ^0.458 0.4 0.3 0.4 0 8 normal
