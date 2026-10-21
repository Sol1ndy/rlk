# heart clip heart_idle (id 33) on heart_tips: 40 t, loop. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 40.. run scoreboard players set @s apOC 0
execute if score @s apOC matches 0 run return run function rlk:mboss/apep/om/heart/c/heart_idle/heart_tips/k/0
execute if score @s apOC matches 8 run return run function rlk:mboss/apep/om/heart/c/heart_idle/heart_tips/k/8
execute if score @s apOC matches 17 run return run function rlk:mboss/apep/om/heart/c/heart_idle/heart_tips/k/17
execute if score @s apOC matches 27 run return run function rlk:mboss/apep/om/heart/c/heart_idle/heart_tips/k/27
execute if score @s apOC matches 37 run return run function rlk:mboss/apep/om/heart/c/heart_idle/heart_tips/k/37
