# re-form on the back: glint at the hilt, then a flat glowing gold silhouette grows from the grip to the tip
function rlk:fx/nv/card {kind:"star",pos:"^-0.162 ^1.597 ^-0.436",rot:"~ ~",bb:"center",roll:0,spin:45,s0:0.06,s1:0.6,move:"0f,0f,0f",life:5,fade:2}
function rlk:fx/nv/card {kind:"shard",pos:"^-0.162 ^1.597 ^-0.436",rot:"~ ~",bb:"fixed",roll:-160,spin:0,s0:0,s1:1.644,move:"0f,0f,0f",life:11,fade:5}
function rlk:fx/nv/card {kind:"shard",pos:"^-0.162 ^1.597 ^-0.436",rot:"~ ~",bb:"fixed",roll:20,spin:0,s0:0,s1:0.447,move:"0f,0f,0f",life:10,fade:5}
execute if score @s nvP matches 1.. run particle minecraft:wax_on ^-0.162 ^1.597 ^-0.386 0.1 0.2 0.1 0 6 normal
