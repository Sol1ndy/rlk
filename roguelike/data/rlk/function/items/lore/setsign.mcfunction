# io.v 부호에 따라 io.sign("+"/""), io.vcolor("green"/"red") 설정 (lore 스탯 표시용)
data modify storage rlk:io sign set value "+"
data modify storage rlk:io vcolor set value "green"
execute store result score #sv tmp run data get storage rlk:io v
execute if score #sv tmp matches ..-1 run data modify storage rlk:io sign set value ""
execute if score #sv tmp matches ..-1 run data modify storage rlk:io vcolor set value "red"
