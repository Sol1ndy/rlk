scoreboard players operation #t1 tmp = @s bol
scoreboard players operation #t1 tmp *= #arUse tmp
scoreboard players operation #t1 tmp /= #1000 tmp
execute if score #t1 tmp matches ..0 run scoreboard players set #t1 tmp 1
scoreboard players operation @s bol -= #t1 tmp
execute if score @s bol matches ..0 run scoreboard players set @s bol 0
function rlk:player/bol/on_change
execute if score @s bol matches 0 run function rlk:player/bol/on_clear
execute if score @s skillCd matches 1.. run scoreboard players operation @s skillCd -= #arCdCut tmp
execute if score @s skillCd matches ..-1 run scoreboard players set @s skillCd 0
