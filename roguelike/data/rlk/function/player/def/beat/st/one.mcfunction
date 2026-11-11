# @s = 세계 쪽 디스플레이 하나
execute store result score #d cb run data get entity @s interpolation_duration
execute if score #d cb matches ..0 run return 0
execute if score #d cb = @s btD run return 0
execute unless data entity @s {shadow_radius:0f} run return 0
scoreboard players operation @s btD0 = #d cb
scoreboard players operation #d cb *= #3 tmp
execute if score #d cb matches 120.. run scoreboard players set #d cb 120
scoreboard players operation @s btD = #d cb
tag @s add rlk_bt_st
execute store result storage rlk:bt d int 1 run scoreboard players get #d cb
function rlk:player/def/beat/st/write with storage rlk:bt
