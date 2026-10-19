# heart clip heart_drop (id 32) on heart_bulb: 30 t, then heart_idle. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 30.. run return run function rlk:mboss/apep/om/heart/c/heart_idle/heart_bulb/enter
execute if score @s apOC matches ..4 run return run function rlk:mboss/apep/om/heart/c/heart_drop/heart_bulb/b/0_4
function rlk:mboss/apep/om/heart/c/heart_drop/heart_bulb/b/5_15
