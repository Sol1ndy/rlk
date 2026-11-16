execute store result storage rlk:bt d int 1 run scoreboard players get @s btTp
function rlk:player/def/beat/st/tp_write {n:"0.96"}
scoreboard players reset @s btTp
tag @s remove rlk_bt_tp
