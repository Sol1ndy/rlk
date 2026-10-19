# wall clip wall_rise (id 44) on wall_blade: 5 t, then stops. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 6.. run return run scoreboard players set @s apOI -1
execute if score @s apOC matches 0 run return run function rlk:mboss/apep/om/wall/c/wall_rise/wall_blade/k/0
execute if score @s apOC matches 1 run return run function rlk:mboss/apep/om/wall/c/wall_rise/wall_blade/k/1
execute if score @s apOC matches 2 run return run function rlk:mboss/apep/om/wall/c/wall_rise/wall_blade/k/2
execute if score @s apOC matches 3 run return run function rlk:mboss/apep/om/wall/c/wall_rise/wall_blade/k/3
