# End of motion/tick: re-apply the snap after the last pose of the tick.
execute if entity @e[tag=rlk_pm_weapon] run data merge entity @e[tag=rlk_pm_weapon,limit=1] {interpolation_duration:0,start_interpolation:0}
scoreboard players set #pmSnapW tmp 0
