function rlk:fx/nv/card {kind:"rose",pos:"^0.2 ^3.64 ^0.43",rot:"~ ~",bb:"center",roll:0,spin:30,s0:0.05,s1:0.28,move:"0f,-0.35f,0f",life:7,fade:3}
function rlk:fx/nv/card {kind:"rose",pos:"^-0.62 ^3.95 ^-0.34",rot:"~ ~",bb:"center",roll:20,spin:-30,s0:0.05,s1:0.26,move:"0f,-0.35f,0f",life:7,fade:3}
function rlk:fx/nv/p/glint {pos:"^-0.2 ^4.05 ^0.14"}
function rlk:fx/nv/card {kind:"petal",pos:"^0.5 ^3.4 ^-0.6",rot:"~ ~",bb:"center",roll:10,spin:150,s0:0.16,s1:0.12,move:"0f,-1.1f,0f",life:30,fade:6}
function rlk:fx/nv/card {kind:"petal",pos:"^-0.6 ^3.2 ^0.7",rot:"~ ~",bb:"center",roll:-50,spin:-150,s0:0.14,s1:0.1,move:"0f,-1.0f,0f",life:28,fade:6}
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.55} ^0.38 ^3.77 ^0.04 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.55} ^0.2 ^3.64 ^0.43 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.55} ^-0.2 ^3.6 ^0.59 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.55} ^-0.62 ^3.67 ^0.44 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.55} ^-0.79 ^3.82 ^0.05 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.55} ^-0.62 ^3.95 ^-0.34 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.55} ^-0.2 ^3.99 ^-0.5 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.55} ^0.2 ^3.92 ^-0.35 0.03 0.03 0.03 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.2 ^3.85 ^0.07 0.5 0.2 0.5 0 8 normal
