# heart clip heart_drop (id 32) on vine_stem_1: 30 t, then heart_idle. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 30.. run return run scoreboard players set @s apOI -1
execute if score @s apOC matches ..20 run return run function rlk:mboss/apep/om/heart/c/heart_drop/vine_stem_1/b/0_20
function rlk:mboss/apep/om/heart/c/heart_drop/vine_stem_1/b/22_29
