# heart clip heart_drop (id 32) on heart_tips: 30 t, then heart_idle. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 30.. run return run function rlk:mboss/apep/om/heart/c/heart_idle/heart_tips/enter
execute if score @s apOC matches 0 run return run function rlk:mboss/apep/om/heart/c/heart_drop/heart_tips/k/0
execute if score @s apOC matches 5 run return run function rlk:mboss/apep/om/heart/c/heart_drop/heart_tips/k/5
execute if score @s apOC matches 6 run return run function rlk:mboss/apep/om/heart/c/heart_drop/heart_tips/k/6
execute if score @s apOC matches 8 run return run function rlk:mboss/apep/om/heart/c/heart_drop/heart_tips/k/8
execute if score @s apOC matches 11 run return run function rlk:mboss/apep/om/heart/c/heart_drop/heart_tips/k/11
execute if score @s apOC matches 16 run return run function rlk:mboss/apep/om/heart/c/heart_drop/heart_tips/k/16
