particle minecraft:dust{color:[0.914,0.725,0.286],scale:1.1} ^0.33 ^1.07 ^1.42 0.04 0.04 0.04 0 2 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:1.1} ^0.28 ^0.79 ^1.54 0.04 0.04 0.04 0 2 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:1.1} ^0.2 ^0.55 ^1.71 0.04 0.04 0.04 0 2 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:1.1} ^0.09 ^0.36 ^1.94 0.04 0.04 0.04 0 2 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.8} ^0.09 ^0.36 ^1.94 0.03 0.03 0.03 0 2 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.8} ^-0.58 ^2.01 ^3.38 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.914,0.725,0.286],scale:0.8} ^-0.39 ^2.44 ^2.98 0.03 0.03 0.03 0 1 normal
function rlk:fx/nv/card {kind:"crescent",pos:"^-0.15 ^1.4 ^2.46",rot:"~205 ~",bb:"fixed",roll:-90,spin:50,s0:2.3,s1:2.7,move:"0f,0f,0f",life:4,fade:2}
function rlk:fx/nv/card {kind:"burst",pos:"^-0.15 ^1.25 ^2.26",rot:"~ ~",bb:"center",roll:35,spin:20,s0:0.45,s1:1.5,move:"0f,0f,0f",life:4,fade:2}
particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.0} ^-0.15 ^1.25 ^2.26 0.2 0.2 0.2 0 6 normal
particle minecraft:crit ^-0.15 ^1.25 ^2.26 0.25 0.25 0.25 0.3 6 normal
function rlk:fx/nv/p/hit_ring {pos:"^-0.15 ^1.25 ^2.26"}
execute if score @s nvP matches 1.. run function rlk:fx/nv/card {kind:"shard",pos:"^0.1 ^0 ^2.36",rot:"~-10 ~",bb:"fixed",roll:-8,spin:0,s0:0,s1:0.9,move:"0f,0f,0f",life:7,fade:3}
execute if score @s nvP matches 1.. run function rlk:fx/nv/card {kind:"shard",pos:"^-0.45 ^0 ^2.56",rot:"~15 ~",bb:"fixed",roll:-10,spin:0,s0:0,s1:0.7,move:"0f,0f,0f",life:7,fade:3}
execute if score @s nvP matches 1.. run particle minecraft:dust{color:[0.965,0.835,0.478],scale:1.2} ^-0.15 ^0.2 ^2.46 0.35 0.35 0.35 0 6 normal
