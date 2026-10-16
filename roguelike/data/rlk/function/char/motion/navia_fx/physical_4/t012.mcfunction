function rlk:fx/nv/card {kind:"glow",pos:"^-0.05 ^0.04 ^1.2",rot:"~ 90",bb:"fixed",roll:0,spin:0,s0:0.6,s1:2.2,move:"0f,0f,0f",life:5,fade:2}
function rlk:fx/nv/card {kind:"glow",pos:"^-0.05 ^0.15 ^2.5",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.5,s1:1.6,move:"0f,0f,0f",life:5,fade:2}
function rlk:fx/nv/card {kind:"shard",pos:"^0.35 ^0 ^2.5",rot:"~ ~",bb:"center",roll:28,spin:0,s0:0,s1:1,move:"0f,0f,0f",life:8,fade:3}
function rlk:fx/nv/card {kind:"shard",pos:"^0.12 ^0 ^2.6",rot:"~-20 ~",bb:"center",roll:10,spin:0,s0:0,s1:1.4,move:"0f,0f,0f",life:8,fade:3}
function rlk:fx/nv/card {kind:"shard",pos:"^-0.15 ^0 ^2.55",rot:"~25 ~",bb:"center",roll:-8,spin:0,s0:0,s1:1.2,move:"0f,0f,0f",life:8,fade:3}
function rlk:fx/nv/card {kind:"shard",pos:"^-0.42 ^0 ^2.45",rot:"~ ~",bb:"center",roll:-30,spin:0,s0:0,s1:0.9,move:"0f,0f,0f",life:8,fade:3}
particle minecraft:block{block_state:"minecraft:gold_block"} ^-0.05 ^0.1 ^2.5 0.4 0.1 0.4 0 12 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.2} ^-0.05 ^0.2 ^2.5 0.25 0.25 0.25 0 6 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:1.0} ^-0.05 ^0.3 ^2.5 0.5 0.5 0.5 0 10 normal
particle minecraft:end_rod ^-0.05 ^0 ^2.5 0.3 0.1 0.3 0.12 6 normal
particle minecraft:dust{color:[0.62,0.58,0.55],scale:1.3} ^0 ^0.05 ^0 0.25 0.25 0.25 0 5 normal
particle minecraft:poof ^0 ^0.05 ^0 0.2 0.02 0.2 0.02 3 normal
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.05 ^0 ^2.5 0.6 0.4 0.6 0 10 normal
execute if score @s nvP matches 1.. run particle minecraft:dust{color:[0.914,0.725,0.286],scale:1.2} ^-0.05 ^0.4 ^2.5 0.5 0.5 0.5 0 8 normal
