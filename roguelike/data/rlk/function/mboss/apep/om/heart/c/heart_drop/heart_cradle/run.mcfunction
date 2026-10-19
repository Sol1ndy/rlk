# heart clip heart_drop (id 32) on heart_cradle: 30 t, then heart_idle. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 30.. run return run scoreboard players set @s apOI -1
execute if score @s apOC matches 0 run return run function rlk:mboss/apep/om/heart/c/heart_drop/heart_cradle/k/0
execute if score @s apOC matches 5 run return run function rlk:mboss/apep/om/heart/c/heart_drop/heart_cradle/k/5
execute if score @s apOC matches 6 run return run function rlk:mboss/apep/om/heart/c/heart_drop/heart_cradle/k/6
execute if score @s apOC matches 7 run return run function rlk:mboss/apep/om/heart/c/heart_drop/heart_cradle/k/7
execute if score @s apOC matches 8 run return run function rlk:mboss/apep/om/heart/c/heart_drop/heart_cradle/k/8
