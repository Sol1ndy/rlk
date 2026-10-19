# Clip sink (id 3) tick 18: the proxy columns that moved.
data modify storage rlk:mboss px.o.core_x set value 0d
data modify storage rlk:mboss px.o.core_z set value 0d
data modify storage rlk:mboss px.top.core set value 0.126f
data merge entity 524c4b4d-4350-4400-8000-000000000041 {height:0.126f}
scoreboard players set #pxU1 mb 0
function rlk:mboss/px/cproto/ev/1
