# (retimed from t017)
particle minecraft:dust{color:[0.914,0.725,0.286],scale:1.1} ^-0.51 ^0.57 ^3.23 0.04 0.04 0.04 0 2 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:1.1} ^-0.59 ^0.82 ^3.4 0.04 0.04 0.04 0 2 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:1.1} ^-0.64 ^1.11 ^3.5 0.04 0.04 0.04 0 2 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:1.1} ^-0.65 ^1.42 ^3.54 0.04 0.04 0.04 0 2 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.8} ^-0.65 ^1.42 ^3.54 0.03 0.03 0.03 0 2 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.8} ^0.29 ^1.98 ^1.52 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.8} ^0.35 ^1.38 ^1.38 0.03 0.03 0.03 0 1 normal
function rlk:fx/nv/card {kind:"crescent",pos:"^-0.15 ^1.4 ^2.46",rot:"~205 ~",bb:"fixed",roll:-90,spin:50,s0:2.3,s1:2.7,move:"0f,0f,0f",life:6,fade:3}
function rlk:fx/nv/card {kind:"burst",pos:"^-0.15 ^1.25 ^2.26",rot:"~ ~",bb:"center",roll:60,spin:20,s0:0.45,s1:1.7000000000000002,move:"0f,0f,0f",life:4,fade:2}
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.0} ^-0.15 ^1.25 ^2.26 0.2 0.2 0.2 0 6 normal
particle minecraft:crit ^-0.15 ^1.25 ^2.26 0.25 0.25 0.25 0.3 6 normal
function rlk:fx/nv/p/hit_ring {pos:"^-0.15 ^1.25 ^2.26"}
execute if score @s nvP matches 1.. run function rlk:fx/nv/card {kind:"shard",pos:"^0.1 ^0 ^2.36",rot:"~-10 ~",bb:"fixed",roll:-28,spin:0,s0:0,s1:0.9,move:"0f,0f,0f",life:7,fade:3}
execute if score @s nvP matches 1.. run function rlk:fx/nv/card {kind:"shard",pos:"^-0.45 ^0 ^2.56",rot:"~15 ~",bb:"fixed",roll:5,spin:0,s0:0,s1:0.7,move:"0f,0f,0f",life:7,fade:3}
execute if score @s nvP matches 1.. run particle minecraft:dust{color:[0.965,0.835,0.478],scale:1.2} ^-0.15 ^0.2 ^2.46 0.35 0.35 0.35 0 6 normal
