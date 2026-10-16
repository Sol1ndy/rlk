# (retimed from t020)
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.45} ^-0.47 ^3.65 ^0.05 0.08 0.08 0.08 0 3 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.5} ^0 ^3.22 ^0 1.0 1.0 1.0 0 2 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.37 ^4.1 ^0.09 0.2 0.2 0.2 0 3 normal
# (retimed from t021)
function rlk:fx/nv/card {kind:"rose",pos:"^-0.03 ^3.69 ^0.39",rot:"~ ~",bb:"center",roll:0,spin:30,s0:0.05,s1:0.28,move:"0f,-0.35f,0f",life:7,fade:3}
function rlk:fx/nv/card {kind:"rose",pos:"^-0.79 ^3.89 ^-0.46",rot:"~ ~",bb:"center",roll:20,spin:-30,s0:0.05,s1:0.26,move:"0f,-0.35f,0f",life:7,fade:3}
function rlk:fx/nv/p/glint {pos:"^-0.35 ^4.05 ^-0.03"}
function rlk:fx/nv/card {kind:"petal",pos:"^0.5 ^3.4 ^-0.6",rot:"~ ~",bb:"center",roll:10,spin:150,s0:0.16,s1:0.12,move:"0f,-1.1f,0f",life:30,fade:6}
function rlk:fx/nv/card {kind:"petal",pos:"^-0.6 ^3.2 ^0.7",rot:"~ ~",bb:"center",roll:-50,spin:-150,s0:0.14,s1:0.1,move:"0f,-1.0f,0f",life:28,fade:6}
