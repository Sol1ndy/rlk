execute store result score #d cb run data get entity @s teleport_duration
execute unless score #d cb matches 1..19 run return 0
execute unless data entity @s {shadow_radius:0f} run return 0
scoreboard players operation @s btTp = #d cb
scoreboard players operation #d cb *= #3 tmp
tag @s add rlk_bt_tp
execute store result storage rlk:bt d int 1 run scoreboard players get #d cb
function rlk:player/def/beat/st/tp_write {n:"0.97"}
