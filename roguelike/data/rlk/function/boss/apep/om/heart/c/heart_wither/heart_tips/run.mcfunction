# heart clip heart_wither (id 36) on heart_tips: 30 t, then stops. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 31.. run return run scoreboard players set @s apOI -1
execute if score @s apOC matches 0 run return run function rlk:boss/apep/om/heart/c/heart_wither/heart_tips/k/0
execute if score @s apOC matches 4 run return run function rlk:boss/apep/om/heart/c/heart_wither/heart_tips/k/4
execute if score @s apOC matches 10 run return run function rlk:boss/apep/om/heart/c/heart_wither/heart_tips/k/10
execute if score @s apOC matches 16 run return run function rlk:boss/apep/om/heart/c/heart_wither/heart_tips/k/16
execute if score @s apOC matches 22 run return run function rlk:boss/apep/om/heart/c/heart_wither/heart_tips/k/22
execute if score @s apOC matches 28 run return run function rlk:boss/apep/om/heart/c/heart_wither/heart_tips/k/28
