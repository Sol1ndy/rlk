scoreboard players operation @s enKey = #enN tmp
execute store result storage rlk:hud ei int 1 run scoreboard players get #enN tmp
function rlk:player/hud/en_set with storage rlk:hud
# 폭발 아이템 이름의 게이지도 다시 만들도록
scoreboard players set @s buShown -1
