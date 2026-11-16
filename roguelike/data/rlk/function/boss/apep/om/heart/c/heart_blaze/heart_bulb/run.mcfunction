# heart clip heart_blaze (id 37) on heart_bulb: 24 t, then stops. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 25.. run return run scoreboard players set @s apOI -1
execute if score @s apOC matches 0 run return run function rlk:boss/apep/om/heart/c/heart_blaze/heart_bulb/k/0
execute if score @s apOC matches 5 run return run function rlk:boss/apep/om/heart/c/heart_blaze/heart_bulb/k/5
execute if score @s apOC matches 10 run return run function rlk:boss/apep/om/heart/c/heart_blaze/heart_bulb/k/10
execute if score @s apOC matches 15 run return run function rlk:boss/apep/om/heart/c/heart_blaze/heart_bulb/k/15
