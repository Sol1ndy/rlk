# heart clip heart_wither (id 36) on heart_bulb: 30 t, then stops. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 31.. run return run scoreboard players set @s apOI -1
execute if score @s apOC matches 0 run return run function rlk:mboss/apep/om/heart/c/heart_wither/heart_bulb/k/0
execute if score @s apOC matches 4 run return run function rlk:mboss/apep/om/heart/c/heart_wither/heart_bulb/k/4
execute if score @s apOC matches 21 run return run function rlk:mboss/apep/om/heart/c/heart_wither/heart_bulb/k/21
