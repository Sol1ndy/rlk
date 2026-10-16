# After the pose of this tick: keep the stowed weapon hidden, then grow it on the back.
scoreboard players remove @s pmShFx 1
execute if score @s pmShFx matches 3.. if entity @e[tag=rlk_pm_weapon] run data merge entity @e[tag=rlk_pm_weapon,limit=1] {start_interpolation:0,interpolation_duration:0,transformation:{scale:[0f,0f,0f]}}
execute if score @s pmShFx matches 2 if score #charN tmp matches 5 if entity @e[tag=rlk_pm_weapon] run data merge entity @e[tag=rlk_pm_weapon,limit=1] {start_interpolation:0,interpolation_duration:1,transformation:{scale:[0.400000f,0.400000f,0.400000f]}}
execute if score @s pmShFx matches 2 if score #charN tmp matches 3 if entity @e[tag=rlk_pm_weapon] run data merge entity @e[tag=rlk_pm_weapon,limit=1] {start_interpolation:0,interpolation_duration:1,transformation:{scale:[0.368000f,0.368000f,0.368000f]}}
execute if score @s pmShFx matches 1 if score #charN tmp matches 5 if entity @e[tag=rlk_pm_weapon] run data merge entity @e[tag=rlk_pm_weapon,limit=1] {start_interpolation:0,interpolation_duration:1,transformation:{scale:[0.750000f,0.750000f,0.750000f]}}
execute if score @s pmShFx matches 1 if score #charN tmp matches 3 if entity @e[tag=rlk_pm_weapon] run data merge entity @e[tag=rlk_pm_weapon,limit=1] {start_interpolation:0,interpolation_duration:1,transformation:{scale:[0.690000f,0.690000f,0.690000f]}}
execute if score @s pmShFx matches 2 if entity @e[tag=rlk_pm_weapon] at @e[tag=rlk_pm_body,limit=1] rotated as @e[tag=rlk_pm_body,limit=1] run function rlk:char/motion/sheath/fx_back
