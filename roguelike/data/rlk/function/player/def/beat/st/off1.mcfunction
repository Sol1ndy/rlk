execute store result score #d cb run data get entity @s interpolation_duration
execute if score #d cb = @s btD store result storage rlk:bt d int 1 run scoreboard players get @s btD0
execute unless score #d cb = @s btD store result storage rlk:bt d int 1 run scoreboard players get #d cb
data modify storage rlk:bt n set value "1"
function rlk:player/def/beat/st/write with storage rlk:bt
scoreboard players reset @s btD
scoreboard players reset @s btD0
tag @s remove rlk_bt_st
