# barrage shell impact: gold flare, sparks, gold flakes
particle minecraft:explosion ^-0.6 ^0.6 ^6.2 0 0 0 0 1 normal
particle minecraft:block{block_state:"minecraft:gold_block"} ^-0.6 ^0.4 ^6.2 0.6 0.3 0.6 0.15 10 normal
particle minecraft:end_rod ^-0.6 ^0.5 ^6.2 0 0 0 0.18 6 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-1.493 ^0.15 ^6.089 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-1.388 ^0.15 ^6.635 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-0.982 ^0.15 ^7.015 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-0.43 ^0.15 ^7.084 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^0.057 ^0.15 ^6.815 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^0.293 ^0.15 ^6.311 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^0.188 ^0.15 ^5.765 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-0.218 ^0.15 ^5.385 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-0.77 ^0.15 ^5.316 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-1.257 ^0.15 ^5.585 0 0 0 0 1 normal
function rlk:fx/nv/card {kind:"burst",pos:"^-0.6 ^0.7 ^6.2",rot:"~ ~",bb:"center",roll:29,spin:18,s0:0.5,s1:1.6,move:"0f,0f,0f",life:4,fade:2}
# dissolve into a stream of gold motes drifting down and back (v1 E13)
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.6} ^-0.413 ^0.809 ^0.133 0.05 0.06 0.05 0 2 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.6} ^-0.436 ^0.738 ^0.156 0.05 0.06 0.05 0 2 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.6} ^-0.459 ^0.667 ^0.179 0.05 0.06 0.05 0 2 normal
particle minecraft:falling_dust{block_state:"minecraft:gold_block"} ^-0.436 ^0.918 ^0.306 0.15 0.15 0.15 0 3 normal
function rlk:fx/nv/card {kind:"star",pos:"^-0.49 ^1.08 ^0.32",rot:"~ ~",bb:"center",roll:0,spin:45,s0:0.04,s1:0.28,move:"0f,0f,0f",life:5,fade:2}
function rlk:fx/nv/card {kind:"star",pos:"^-0.37 ^1.22 ^0.3",rot:"~ ~",bb:"center",roll:0,spin:45,s0:0.04,s1:0.28,move:"0f,0f,0f",life:5,fade:2}
particle minecraft:end_rod ^-0.39 ^1.06 ^0.26 0.1 0.1 0.1 0.01 3 normal
