# sweep_e clip tick 20
execute if entity @e[type=minecraft:marker,tag=rlk_mb_gd_p12h,scores={mbHzHit=1..}] run scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_gd_p12h] mbHzHit 1
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p12b1]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p12w3] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[0.984f,0.01f,0.04f]}}
execute if score #gdSwEl mb matches 1 run function rlk:mboss/guardian/p/sweep_e/s4_1
execute if score #gdSwEl mb matches 2 run function rlk:mboss/guardian/p/sweep_e/s4_2
execute if score #gdSwEl mb matches 3 run function rlk:mboss/guardian/p/sweep_e/s4_3
execute if score #gdSwEl mb matches 4 run function rlk:mboss/guardian/p/sweep_e/s4_4
