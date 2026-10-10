# 누른 채 반복되는 입력은 무시하고, 놓았다 다시 누르면 동작한다.
scoreboard players set #mapHeld view 0
execute if score @s vMapR matches 1.. run scoreboard players set #mapHeld view 1
scoreboard players set @s vMapR 6
execute if score #mapHeld view matches 1 run return 0
function rlk:view/map_toggle
