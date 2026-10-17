# sweep_e clip tick 23
execute if entity @e[type=minecraft:marker,tag=rlk_mb_gd_p12h,scores={mbHzHit=1..}] run scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_gd_p12h] mbHzHit 1
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p12w1] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[0.82f,0.01f,0.04f]}}
execute if score #gdSwEl mb matches 1 run function rlk:mboss/guardian/p/sweep_e/s2_1
execute if score #gdSwEl mb matches 2 run function rlk:mboss/guardian/p/sweep_e/s2_2
execute if score #gdSwEl mb matches 3 run function rlk:mboss/guardian/p/sweep_e/s2_3
execute if score #gdSwEl mb matches 4 run function rlk:mboss/guardian/p/sweep_e/s2_4
execute if score #gdSwEl mb matches 1 run playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 0.9 0.8 0.3
execute if score #gdSwEl mb matches 1 run playsound minecraft:entity.blaze.shoot hostile @a[tag=player] ~ ~ ~ 0.45 0.7 0.15
execute if score #gdSwEl mb matches 2 run playsound minecraft:entity.player.splash.high_speed hostile @a[tag=player] ~ ~ ~ 0.9 1 0.3
execute if score #gdSwEl mb matches 2 run playsound minecraft:entity.generic.splash hostile @a[tag=player] ~ ~ ~ 0.5 1.3 0.17
execute if score #gdSwEl mb matches 3 run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.5 1.8 0.17
execute if score #gdSwEl mb matches 4 run playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 0.9 1.3 0.3
execute if score #gdSwEl mb matches 4 run playsound minecraft:block.powder_snow.break hostile @a[tag=player] ~ ~ ~ 1 1 0.33
