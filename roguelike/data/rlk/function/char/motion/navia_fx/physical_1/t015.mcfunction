# (retimed from t013)
particle minecraft:block{block_state:"minecraft:gold_block"} ^1.23 ^0.06 ^-0.77 0.25 0.04 0.25 0.12 10 normal
particle minecraft:poof ^1.23 ^0.06 ^-0.77 0.2 0.02 0.2 0.015 4 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:1} ^1.23 ^0.06 ^-0.77 0.3 0.3 0.3 0 6 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^1.23 ^0.25 ^-0.77 0.3 0.15 0.3 0 5 normal
