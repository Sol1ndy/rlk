# @s = a new aux (aux/setup) with #auxResEl mb 0..8: mbRes0..8 = #auxRes, mbRes<#auxResEl> = #auxResElV, rlk_mb_resel.
scoreboard players operation @s mbRes0 = #auxRes mb
scoreboard players operation @s mbRes1 = #auxRes mb
scoreboard players operation @s mbRes2 = #auxRes mb
scoreboard players operation @s mbRes3 = #auxRes mb
scoreboard players operation @s mbRes4 = #auxRes mb
scoreboard players operation @s mbRes5 = #auxRes mb
scoreboard players operation @s mbRes6 = #auxRes mb
scoreboard players operation @s mbRes7 = #auxRes mb
scoreboard players operation @s mbRes8 = #auxRes mb
execute if score #auxResEl mb matches 0 run scoreboard players operation @s mbRes0 = #auxResElV mb
execute if score #auxResEl mb matches 1 run scoreboard players operation @s mbRes1 = #auxResElV mb
execute if score #auxResEl mb matches 2 run scoreboard players operation @s mbRes2 = #auxResElV mb
execute if score #auxResEl mb matches 3 run scoreboard players operation @s mbRes3 = #auxResElV mb
execute if score #auxResEl mb matches 4 run scoreboard players operation @s mbRes4 = #auxResElV mb
execute if score #auxResEl mb matches 5 run scoreboard players operation @s mbRes5 = #auxResElV mb
execute if score #auxResEl mb matches 6 run scoreboard players operation @s mbRes6 = #auxResElV mb
execute if score #auxResEl mb matches 7 run scoreboard players operation @s mbRes7 = #auxResElV mb
execute if score #auxResEl mb matches 8 run scoreboard players operation @s mbRes8 = #auxResElV mb
tag @s add rlk_mb_resel
