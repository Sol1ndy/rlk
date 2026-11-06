# Clip burrow_strike (id 7) tick 14: the proxy columns that moved.
data modify storage rlk:mboss px.o.head_x set value 0d
data modify storage rlk:mboss px.o.head_z set value 3.43d
data modify storage rlk:mboss px.top.head set value 0f
data merge entity 524c4b4d-4150-4400-8000-000000000041 {height:0.1f}
data modify storage rlk:mboss px.o.chest_x set value 0d
data modify storage rlk:mboss px.o.chest_z set value -0.09d
data modify storage rlk:mboss px.top.chest set value 0.26f
data merge entity 524c4b4d-4150-4400-8000-000000000042 {height:0.26f}
scoreboard players set #pxU2 mb 0
function rlk:mboss/px/apep/ev/2
