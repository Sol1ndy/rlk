# Clip death (id 35) tick 108: the proxy columns that moved.
data modify storage rlk:mboss px.o.chest_x set value 0d
data modify storage rlk:mboss px.o.chest_z set value 0.4d
data modify storage rlk:mboss px.top.chest set value 0.46f
data merge entity 524c4b4d-4150-4400-8000-000000000042 {height:0.46f}
data modify storage rlk:mboss px.o.abd_x set value 0d
data modify storage rlk:mboss px.o.abd_z set value -1.45d
data modify storage rlk:mboss px.top.abd set value 0.05f
data merge entity 524c4b4d-4150-4400-8000-000000000043 {height:0.1f}
data modify storage rlk:mboss px.o.b_l_x set value 3.75d
data modify storage rlk:mboss px.o.b_l_z set value 2.99d
data modify storage rlk:mboss px.top.b_l set value 0.07f
data merge entity 524c4b4d-4150-4400-8000-000000000047 {height:0.1f}
scoreboard players set #pxU7 mb 0
function rlk:mboss/px/apep/ev/7
data modify storage rlk:mboss px.o.b_r_x set value -3.75d
data modify storage rlk:mboss px.o.b_r_z set value 2.99d
data modify storage rlk:mboss px.top.b_r set value 0.07f
data merge entity 524c4b4d-4150-4400-8000-00000000004a {height:0.1f}
scoreboard players set #pxU10 mb 0
function rlk:mboss/px/apep/ev/10
