# barrage shell (cosmetic): comet streak
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.8} ^3 ^4.2 ^1.5 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.8} ^2.867 ^3.85 ^1.592 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.8} ^2.733 ^3.5 ^1.683 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.8} ^2.6 ^3.15 ^1.775 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.8} ^2.467 ^2.8 ^1.867 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.8} ^2.333 ^2.45 ^1.958 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.8} ^2.2 ^2.1 ^2.05 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.8} ^2.067 ^1.75 ^2.142 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.8} ^1.933 ^1.4 ^2.233 0 0 0 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.8} ^1.8 ^1.05 ^2.325 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.2} ^1.667 ^0.7 ^2.417 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.2} ^1.533 ^0.35 ^2.508 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.2} ^1.4 ^0 ^2.6 0 0 0 0 1 normal
# cane tap: the ferrule touches down in front of the right foot
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.8} ^-0.397 ^0.06 ^0.393 0.12 0.01 0.12 0 6 normal
particle minecraft:wax_on ^-0.397 ^0.1 ^0.393 0.15 0.05 0.15 0 3 normal
execute if score @s nvP matches 1.. run particle minecraft:electric_spark ^-0.397 ^0.08 ^0.393 0.1 0.02 0.1 0.05 4 normal
