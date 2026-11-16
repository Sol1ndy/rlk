# heart clip heart_gain (id 35) on heart_tips: 8 t, then heart_idle. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 8.. run return run function rlk:boss/apep/om/heart/c/heart_idle/heart_tips/enter
execute if score @s apOC matches 0 run return run function rlk:boss/apep/om/heart/c/heart_gain/heart_tips/k/0
execute if score @s apOC matches 1 run return run function rlk:boss/apep/om/heart/c/heart_gain/heart_tips/k/1
execute if score @s apOC matches 2 run return run function rlk:boss/apep/om/heart/c/heart_gain/heart_tips/k/2
