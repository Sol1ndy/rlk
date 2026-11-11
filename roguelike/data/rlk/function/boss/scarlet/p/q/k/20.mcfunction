# Q pattern tick 20
kill @e[type=minecraft:item_display,tag=rlk_hr_swlh]
execute as @e[type=minecraft:item_display,tag=rlk_hr_swl] run data merge entity @s {item:{components:{"minecraft:custom_model_data":{colors:[16777215]}}}}
kill @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_m20,limit=1]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_m20] run data merge entity @s {item:{components:{"minecraft:custom_model_data":{colors:[16777215]}}}}
function rlk:boss/scarlet/rig/look/form/normal
tag @s remove rlk_hr_ghost
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ 202 ~ run function rlk:boss/scarlet/fx/p/claw_streaks {r:12}
