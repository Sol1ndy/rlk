particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.5} ^-1.58 ^1.01 ^0.64 0.04 0.04 0.04 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.5} ^-1.19 ^1.25 ^-0.28 0.04 0.04 0.04 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.5} ^-0.63 ^2 ^0.16 0.04 0.04 0.04 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.5} ^-1.02 ^1.76 ^1.08 0.04 0.04 0.04 0 1 normal
function rlk:fx/nv/p/rose_pop {pos:"^-0.83 ^1.67 ^-0.25"}
particle minecraft:wax_on ^-1.16 ^1.55 ^0.39 0.5 0.3 0.5 0 3 normal
execute if score @s nvP matches 1.. run particle minecraft:electric_spark ^-1.16 ^1.55 ^0.39 0.5 0.3 0.5 0.05 4 normal
