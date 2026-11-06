# Clip emerge_crown_p1 (id 11) tick 5: the proxy columns that moved.
data modify storage rlk:mboss px.o.head_x set value 0d
data modify storage rlk:mboss px.o.head_z set value 2.99d
data modify storage rlk:mboss px.top.head set value 0.71f
data merge entity 524c4b4d-4150-4400-8000-000000000041 {height:0.71f}
scoreboard players set #pxU1 mb 1
function rlk:mboss/px/apep/ev/1
data modify storage rlk:mboss px.o.chest_x set value 0d
data modify storage rlk:mboss px.o.chest_z set value 0.87d
data modify storage rlk:mboss px.top.chest set value 0.47f
data merge entity 524c4b4d-4150-4400-8000-000000000042 {height:0.47f}
scoreboard players set #pxU2 mb 1
function rlk:mboss/px/apep/ev/2
