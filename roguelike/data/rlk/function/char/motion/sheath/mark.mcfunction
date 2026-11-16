# Grip position of the displayed weapon for the stow sparkle (sheathed clip starts mark before frame zero).
execute store result storage rlk:player_motion spark.x double 0.001 run data get entity @e[tag=rlk_pm_weapon,limit=1] transformation.translation[0] 1000
execute store result storage rlk:player_motion spark.y double 0.001 run data get entity @e[tag=rlk_pm_weapon,limit=1] transformation.translation[1] 1000
execute store result storage rlk:player_motion spark.z double 0.001 run data get entity @e[tag=rlk_pm_weapon,limit=1] transformation.translation[2] 1000
