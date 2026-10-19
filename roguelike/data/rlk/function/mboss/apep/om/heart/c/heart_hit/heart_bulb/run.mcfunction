# heart clip heart_hit (id 34) on heart_bulb: 6 t, then heart_idle. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 6.. run return run function rlk:mboss/apep/om/heart/c/heart_idle/heart_bulb/enter
execute if score @s apOC matches 0 run return run function rlk:mboss/apep/om/heart/c/heart_hit/heart_bulb/k/0
execute if score @s apOC matches 1 run return run function rlk:mboss/apep/om/heart/c/heart_hit/heart_bulb/k/1
execute if score @s apOC matches 3 run return run function rlk:mboss/apep/om/heart/c/heart_hit/heart_bulb/k/3
