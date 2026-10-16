# barrage shell impact: gold flare, sparks, gold flakes
particle minecraft:explosion ^-2.6 ^0.6 ^5.6 0 0 0 0 1 normal
particle minecraft:block{block_state:"minecraft:gold_block"} ^-2.6 ^0.4 ^5.6 0.6 0.3 0.6 0.15 10 normal
particle minecraft:end_rod ^-2.6 ^0.5 ^5.6 0 0 0 0.18 6 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-2.1 ^0.15 ^6.349 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-1.756 ^0.15 ^5.912 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-1.734 ^0.15 ^5.356 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-2.042 ^0.15 ^4.894 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-2.564 ^0.15 ^4.701 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-3.1 ^0.15 ^4.851 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-3.444 ^0.15 ^5.288 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-3.466 ^0.15 ^5.844 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-3.158 ^0.15 ^6.306 0 0 0 0 1 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1} ^-2.636 ^0.15 ^6.499 0 0 0 0 1 normal
function rlk:fx/nv/card {kind:"burst",pos:"^-2.6 ^0.7 ^5.6",rot:"~ ~",bb:"center",roll:1,spin:18,s0:0.5,s1:1.6,move:"0f,0f,0f",life:4,fade:2}
# the canopy snaps shut: motes pulled in along the folded parasol
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.6} ^-0.418 ^0.82 ^0.222 0.08 0.05 0.08 0 2 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.6} ^-0.443 ^0.7 ^0.197 0.08 0.05 0.08 0 2 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.6} ^-0.468 ^0.581 ^0.172 0.08 0.05 0.08 0 2 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.6} ^-0.494 ^0.461 ^0.147 0.08 0.05 0.08 0 2 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.6} ^-0.519 ^0.341 ^0.121 0.08 0.05 0.08 0 2 normal
function rlk:fx/nv/card {kind:"star",pos:"^-0.468 ^0.581 ^0.172",rot:"~ ~",bb:"center",roll:0,spin:45,s0:0.05,s1:0.4,move:"0f,0f,0f",life:5,fade:2}
