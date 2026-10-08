# 생명의 계약을 전부 없앤다 (@s = 플레이어). 없앤 양 → #bolWas tmp (0 이면 없었음)
execute unless score @s bol matches 0.. run scoreboard players set @s bol 0
scoreboard players operation #bolWas tmp = @s bol
execute if score #bolWas tmp matches ..0 run return 0
scoreboard players set @s bol 0
function rlk:player/bol/on_change
function rlk:player/bol/on_clear
