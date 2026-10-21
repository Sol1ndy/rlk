# heart clip heart_up (id 30) on vine_stem_0: 30 t, then heart_hang. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 30.. run return run function rlk:boss/apep/om/heart/c/heart_hang/vine_stem_0/enter
execute if score @s apOC matches 0 run return run function rlk:boss/apep/om/heart/c/heart_up/vine_stem_0/k/0
execute if score @s apOC matches 7 run return run function rlk:boss/apep/om/heart/c/heart_up/vine_stem_0/k/7
execute if score @s apOC matches 15 run return run function rlk:boss/apep/om/heart/c/heart_up/vine_stem_0/k/15
execute if score @s apOC matches 22 run return run function rlk:boss/apep/om/heart/c/heart_up/vine_stem_0/k/22
execute if score @s apOC matches 28 run return run function rlk:boss/apep/om/heart/c/heart_up/vine_stem_0/k/28
