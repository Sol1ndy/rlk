# Clip sink_p1 (id 8) tick 9: the proxy columns that moved.
data modify storage rlk:mboss px.o.head_x set value 0d
data modify storage rlk:mboss px.o.head_z set value 3.4d
data modify storage rlk:mboss px.top.head set value 0.12f
data merge entity 524c4b4d-4150-4400-8000-000000000041 {height:0.12f}
scoreboard players set #pxU1 mb 0
function rlk:mboss/px/apep/ev/1
data modify storage rlk:mboss px.o.chest_x set value 0d
data modify storage rlk:mboss px.o.chest_z set value -0.1d
data modify storage rlk:mboss px.top.chest set value 0.59f
data merge entity 524c4b4d-4150-4400-8000-000000000042 {height:0.59f}
data modify storage rlk:mboss px.o.abd_x set value 0d
data modify storage rlk:mboss px.o.abd_z set value -2.07d
data modify storage rlk:mboss px.top.abd set value 0f
data merge entity 524c4b4d-4150-4400-8000-000000000043 {height:0.1f}
scoreboard players set #pxU3 mb 0
function rlk:mboss/px/apep/ev/3
