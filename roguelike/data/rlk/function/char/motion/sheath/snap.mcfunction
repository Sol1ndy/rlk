# The weapon jumps to its new attach this tick (no hand/back/world interpolation); repeated at the end of motion/tick.
execute if entity @e[tag=rlk_pm_weapon] run data merge entity @e[tag=rlk_pm_weapon,limit=1] {interpolation_duration:0,start_interpolation:0}
scoreboard players set #pmSnapW tmp 1
