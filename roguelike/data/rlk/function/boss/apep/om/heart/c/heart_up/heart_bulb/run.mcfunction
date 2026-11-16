# heart clip heart_up (id 30) on heart_bulb: 30 t, then heart_hang. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 30.. run return run function rlk:boss/apep/om/heart/c/heart_hang/heart_bulb/enter
execute if score @s apOC matches ..8 run return run function rlk:boss/apep/om/heart/c/heart_up/heart_bulb/b/0_8
function rlk:boss/apep/om/heart/c/heart_up/heart_bulb/b/11_29
