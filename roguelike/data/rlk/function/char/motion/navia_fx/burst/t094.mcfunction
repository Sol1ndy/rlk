# (retimed from t044)
# cane tap: the ferrule touches down in front of the right foot
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.8} ^-0.397 ^0.06 ^0.393 0.12 0.01 0.12 0 6 normal
particle minecraft:wax_on ^-0.397 ^0.1 ^0.393 0.15 0.05 0.15 0 3 normal
execute if score @s nvP matches 1.. run particle minecraft:electric_spark ^-0.397 ^0.08 ^0.393 0.1 0.02 0.1 0.05 4 normal
