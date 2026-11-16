# (retimed from t010)
function rlk:fx/nv/card {kind:"star",pos:"^-0.19 ^0.71 ^0.77",rot:"~ ~",bb:"center",roll:12,spin:30,s0:0.3,s1:0.95,move:"0f,0f,0f",life:4,fade:2}
function rlk:fx/nv/card {kind:"shard",pos:"^-0.19 ^0.71 ^0.77",rot:"~ ~",bb:"fixed",roll:-58,spin:0,s0:0,s1:0.8,move:"0f,0f,0f",life:6,fade:3}
function rlk:fx/nv/card {kind:"shard",pos:"^-0.19 ^0.71 ^0.77",rot:"~-15 ~",bb:"fixed",roll:18,spin:0,s0:0,s1:1.0,move:"0f,0f,0f",life:6,fade:3}
function rlk:fx/nv/card {kind:"shard",pos:"^-0.19 ^0.71 ^0.77",rot:"~20 ~",bb:"fixed",roll:128,spin:0,s0:0,s1:0.7,move:"0f,0f,0f",life:6,fade:3}
function rlk:fx/nv/card {kind:"crescent",pos:"^0 ^0.85 ^0.15",rot:"~ ~",bb:"fixed",roll:0,spin:40,s0:3.0,s1:3.8,move:"0f,0f,0f",life:8,fade:3}
particle minecraft:dust{color:[0.965,0.835,0.478],scale:1.0} ^-0.19 ^0.71 ^0.77 0.18 0.18 0.18 0 10 normal
particle minecraft:dust{color:[1.0,0.953,0.769],scale:0.7} ^-0.19 ^0.71 ^0.77 0.08 0.08 0.08 0 5 normal
particle minecraft:crit ^-0.19 ^0.71 ^0.77 0.15 0.15 0.15 0.35 8 normal
particle minecraft:end_rod ^-0.19 ^0.71 ^0.77 0.1 0.1 0.1 0.06 3 normal
execute if score @s nvP matches 1.. run particle minecraft:end_rod ^-0.19 ^0.71 ^0.77 0.3 0.2 0.3 0.04 4 normal
execute if score @s nvP matches 1.. run particle minecraft:dust{color:[1.0,0.953,0.769],scale:1.1} ^-0.19 ^0.71 ^0.77 0.25 0.25 0.25 0 8 normal
