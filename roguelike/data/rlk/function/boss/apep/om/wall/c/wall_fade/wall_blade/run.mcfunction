# wall clip wall_fade (id 45) on wall_blade: 8 t, then stops. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 9.. run return run scoreboard players set @s apOI -1
execute if score @s apOC matches ..3 run return run function rlk:boss/apep/om/wall/c/wall_fade/wall_blade/b/0_3
function rlk:boss/apep/om/wall/c/wall_fade/wall_blade/b/4_7
