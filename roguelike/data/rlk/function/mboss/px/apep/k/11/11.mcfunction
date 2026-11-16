# Clip emerge_crown_p1 (id 11) tick 11: the proxy columns that moved.
data modify storage rlk:mboss px.o.head_x set value 0d
data modify storage rlk:mboss px.o.head_z set value 3.05d
data modify storage rlk:mboss px.top.head set value 2.63f
data merge entity 524c4b4d-4150-4400-8000-000000000041 {height:2.63f}
data modify storage rlk:mboss px.o.chest_x set value 0d
data modify storage rlk:mboss px.o.chest_z set value 0.83d
data modify storage rlk:mboss px.top.chest set value 2.45f
data merge entity 524c4b4d-4150-4400-8000-000000000042 {height:2.45f}
data modify storage rlk:mboss px.o.a_l_x set value 2.53d
data modify storage rlk:mboss px.o.a_l_z set value 1.4d
data modify storage rlk:mboss px.top.a_l set value 0f
data merge entity 524c4b4d-4150-4400-8000-000000000046 {height:0.1f}
data modify storage rlk:mboss px.o.b_l_x set value 2.02d
data modify storage rlk:mboss px.o.b_l_z set value 2.26d
data modify storage rlk:mboss px.top.b_l set value 0.5f
data merge entity 524c4b4d-4150-4400-8000-000000000047 {height:0.5f}
scoreboard players set #pxU7 mb 1
function rlk:mboss/px/apep/ev/7
data modify storage rlk:mboss px.o.a_r_x set value -2.53d
data modify storage rlk:mboss px.o.a_r_z set value 1.4d
data modify storage rlk:mboss px.top.a_r set value 0f
data merge entity 524c4b4d-4150-4400-8000-000000000049 {height:0.1f}
data modify storage rlk:mboss px.o.b_r_x set value -2.02d
data modify storage rlk:mboss px.o.b_r_z set value 2.26d
data modify storage rlk:mboss px.top.b_r set value 0.5f
data merge entity 524c4b4d-4150-4400-8000-00000000004a {height:0.5f}
scoreboard players set #pxU10 mb 1
function rlk:mboss/px/apep/ev/10
