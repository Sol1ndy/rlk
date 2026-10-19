# heart clip heart_idle (id 33) on heart_bulb: 40 t, loop. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 40.. run scoreboard players set @s apOC 0
execute if score @s apOC matches 0 run return run function rlk:mboss/apep/om/heart/c/heart_idle/heart_bulb/k/0
execute if score @s apOC matches 13 run return run function rlk:mboss/apep/om/heart/c/heart_idle/heart_bulb/k/13
execute if score @s apOC matches 23 run return run function rlk:mboss/apep/om/heart/c/heart_idle/heart_bulb/k/23
execute if score @s apOC matches 34 run return run function rlk:mboss/apep/om/heart/c/heart_idle/heart_bulb/k/34
