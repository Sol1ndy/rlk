# stalk clip leg_slam (id 47) on stalk_high: 6 t, then stops. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 7.. run return run scoreboard players set @s apOI -1
execute if score @s apOC matches 0 run return run function rlk:mboss/apep/om/stalk/c/leg_slam/stalk_high/k/0
execute if score @s apOC matches 1 run return run function rlk:mboss/apep/om/stalk/c/leg_slam/stalk_high/k/1
execute if score @s apOC matches 2 run return run function rlk:mboss/apep/om/stalk/c/leg_slam/stalk_high/k/2
execute if score @s apOC matches 3 run return run function rlk:mboss/apep/om/stalk/c/leg_slam/stalk_high/k/3
execute if score @s apOC matches 4 run return run function rlk:mboss/apep/om/stalk/c/leg_slam/stalk_high/k/4
execute if score @s apOC matches 5 run return run function rlk:mboss/apep/om/stalk/c/leg_slam/stalk_high/k/5
