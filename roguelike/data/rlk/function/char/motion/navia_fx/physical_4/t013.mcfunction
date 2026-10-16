function rlk:fx/nv/card {kind:"crescent",pos:"^0 ^1.4 ^0.1",rot:"~-70 ~",bb:"fixed",roll:90,spin:60,s0:4.5,s1:5.5,move:"0f,0f,0f",life:7,fade:2}
function rlk:fx/nv/card {kind:"shard",pos:"^0.22 ^0 ^2.7",rot:"~-10 ~",bb:"center",roll:14,spin:0,s0:0,s1:1.6,move:"0f,0f,0f",life:7,fade:3}
function rlk:fx/nv/card {kind:"shard",pos:"^-0.3 ^0 ^2.6",rot:"~15 ~",bb:"center",roll:-18,spin:0,s0:0,s1:1.3,move:"0f,0f,0f",life:7,fade:3}
function rlk:fx/nv/p/glint {pos:"^-0.08 ^2.92 ^-1.09"}
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.9} ^-0.05 ^0.8 ^2.5 0.3 0.3 0.3 0 6 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.6} ^-0.05 ^1.2 ^2.5 0.2 0.2 0.2 0 4 normal
execute if score @s nvP matches 1.. run function rlk:fx/nv/card {kind:"shard",pos:"^0 ^0 ^2.35",rot:"~5 ~",bb:"center",roll:0,spin:0,s0:0,s1:1.1,move:"0f,0f,0f",life:7,fade:3}
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.8} ^-0.12 ^2.6 ^0.53 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.8} ^-0.11 ^2.68 ^0.13 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.8} ^-0.1 ^2.76 ^-0.28 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.8} ^-0.09 ^2.84 ^-0.68 0.03 0.03 0.03 0 1 normal
particle minecraft:dust{color:[0.965,0.835,0.478],scale:0.8} ^-0.08 ^2.92 ^-1.09 0.03 0.03 0.03 0 1 normal
