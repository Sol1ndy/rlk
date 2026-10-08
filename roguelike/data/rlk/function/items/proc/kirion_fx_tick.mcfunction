# @s = 플레이어, at @s. 빨간 나선 2개 상승 회전 (30틱). 진행 = 30 - kirionFxT
scoreboard players set #kfa tmp 30
scoreboard players operation #kfa tmp -= @s kirionFxT
scoreboard players operation #kfb tmp = #kfa tmp
scoreboard players operation #kfa tmp *= #st48 tmp
scoreboard players operation #kfb tmp *= #st6 tmp
execute store result storage rlk:kfx ang float 1 run scoreboard players get #kfa tmp
execute store result storage rlk:kfx hy float 0.01 run scoreboard players get #kfb tmp
function rlk:items/proc/kirion_fx_do with storage rlk:kfx
