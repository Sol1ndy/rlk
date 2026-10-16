# barrage shell impact: gold flare, sparks, gold flakes
particle minecraft:explosion ^1.4 ^0.6 ^2.6 0 0 0 0 1 normal
particle minecraft:block{block_state:"minecraft:gold_block"} ^1.4 ^0.4 ^2.6 0.6 0.3 0.6 0.15 10 normal
particle minecraft:end_rod ^1.4 ^0.5 ^2.6 0 0 0 0.18 6 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^1.873 ^0.15 ^1.834 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^1.332 ^0.15 ^1.703 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^0.818 ^0.15 ^1.914 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^0.526 ^0.15 ^2.387 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^0.567 ^0.15 ^2.942 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^0.927 ^0.15 ^3.366 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^1.468 ^0.15 ^3.497 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^1.982 ^0.15 ^3.286 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^2.274 ^0.15 ^2.813 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^2.233 ^0.15 ^2.258 0 0 0 0 1 normal
function rlk:fx/nv/card {kind:"burst",pos:"^1.4 ^0.7 ^2.6",rot:"~ ~",bb:"center",roll:15,spin:18,s0:0.5,s1:1.6,move:"0f,0f,0f",life:4,fade:2}
# dissolve into a stream of gold motes drifting down and back (v1 E13)
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.6} ^-0.431 ^0.824 ^0.281 0.05 0.06 0.05 0 2 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.6} ^-0.482 ^0.668 ^0.332 0.05 0.06 0.05 0 2 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.6} ^-0.533 ^0.512 ^0.383 0.05 0.06 0.05 0 2 normal
particle minecraft:falling_dust{block_state:"minecraft:gold_block"} ^-0.482 ^0.728 ^0.382 0.15 0.15 0.15 0 3 normal
