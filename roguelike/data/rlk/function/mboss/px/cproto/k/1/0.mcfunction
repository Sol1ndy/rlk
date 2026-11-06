# Clip idle (id 1) tick 0: the proxy columns that moved.
data modify storage rlk:mboss px.o.core_x set value 0d
data modify storage rlk:mboss px.o.core_z set value 0d
data modify storage rlk:mboss px.top.core set value 2.4f
data merge entity 524c4b4d-4350-4400-8000-000000000041 {height:2.4f}
scoreboard players set #pxU1 mb 1
function rlk:mboss/px/cproto/ev/1
data modify storage rlk:mboss px.o.tail_x set value 0d
data modify storage rlk:mboss px.o.tail_z set value -2.4d
data modify storage rlk:mboss px.top.tail set value 1.2f
data merge entity 524c4b4d-4350-4400-8000-000000000042 {height:1.2f}
scoreboard players set #pxU2 mb 1
function rlk:mboss/px/cproto/ev/2
