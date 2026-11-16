# @s = a basic to link (#apY links left, #apX = the 양육's id).
execute if score #apY mb matches ..0 run return 0
scoreboard players operation @s apL = #apX mb
function rlk:boss/apep/org/basic/buff_on
scoreboard players remove #apY mb 1
