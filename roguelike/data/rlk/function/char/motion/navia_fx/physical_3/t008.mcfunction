# (retimed from t008)
function rlk:fx/nv/p/glint {pos:"^-0.3 ^1.77 ^0.58"}
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.6} ^-0.3 ^1.77 ^0.58 0.05 0.05 0.05 0 3 normal
execute if score @s nvP matches 1.. run particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.6} ^-0.3 ^1.81 ^0.57 0.05 0.05 0.05 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.6} ^-0.3 ^1.14 ^0.83 0.05 0.05 0.05 0 1 normal
execute if score @s nvP matches 1.. run particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.6} ^-0.3 ^0.48 ^1.1 0.05 0.05 0.05 0 1 normal
