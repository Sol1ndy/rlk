particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.5} ^-1.57 ^1.03 ^0.7 0.04 0.04 0.04 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.5} ^-1.23 ^1.21 ^-0.25 0.04 0.04 0.04 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.5} ^-0.64 ^1.97 ^0.1 0.04 0.04 0.04 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.5} ^-0.98 ^1.8 ^1.05 0.04 0.04 0.04 0 1 normal
function rlk:fx/nv/p/rose_pop {pos:"^-0.87 ^1.63 ^-0.27"}
particle minecraft:wax_on ^-1.16 ^1.55 ^0.39 0.5 0.3 0.5 0 3 normal
execute if score @s nvP matches 1.. run particle minecraft:electric_spark ^-1.16 ^1.55 ^0.39 0.5 0.3 0.5 0.05 4 normal
