# heart clip heart_drop (id 32) on vine_stem_3: 30 t, then heart_idle. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 30.. run return run scoreboard players set @s apOI -1
execute if score @s apOC matches ..19 run return run function rlk:boss/apep/om/heart/c/heart_drop/vine_stem_3/b/0_19
function rlk:boss/apep/om/heart/c/heart_drop/vine_stem_3/b/20_29
