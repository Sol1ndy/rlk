execute store result storage rlk:pinv slnum int 1 run scoreboard players get #si tmp
function rlk:player/inv/place_items_clear_do with storage rlk:pinv
scoreboard players add #si tmp 1
function rlk:player/inv/place_items_clear
