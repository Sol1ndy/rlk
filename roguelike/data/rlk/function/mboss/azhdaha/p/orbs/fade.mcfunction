# The orbit is over: the props shrink away (harmless from now).
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p31d] run data merge entity @s {start_interpolation:0,interpolation_duration:10,transformation:{scale:[0f,0f,0f]}}
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p31d,limit=1] run function rlk:mboss/azhdaha/fx/p/splash
