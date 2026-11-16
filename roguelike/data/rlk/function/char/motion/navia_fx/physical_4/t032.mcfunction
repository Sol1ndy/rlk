# (retimed from t032)
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.5} ^-1.61 ^1.16 ^0.66 0.04 0.04 0.04 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.5} ^-1.27 ^1.37 ^-0.14 0.04 0.04 0.04 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.5} ^-0.78 ^2.02 ^0.23 0.04 0.04 0.04 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.5} ^-1.12 ^1.81 ^1.03 0.04 0.04 0.04 0 1 normal
function rlk:fx/nv/p/rose_pop {pos:"^-0.95 ^1.74 ^-0.12"}
particle minecraft:wax_on ^-1.24 ^1.63 ^0.44 0.5 0.3 0.5 0 3 normal
execute if score @s nvP matches 1.. run particle minecraft:electric_spark ^-1.24 ^1.63 ^0.44 0.5 0.3 0.5 0.05 4 normal
