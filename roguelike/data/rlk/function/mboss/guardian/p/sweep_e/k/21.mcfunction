# sweep_e clip tick 21
execute if entity @e[type=minecraft:marker,tag=rlk_mb_gd_p12h,scores={mbHzHit=1..}] run scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_gd_p12h] mbHzHit 1
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p12w0]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p12w4] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[0.984f,0.01f,0.04f]}}
execute if score #gdSwEl mb matches 1 run function rlk:mboss/guardian/p/sweep_e/s5_1
execute if score #gdSwEl mb matches 2 run function rlk:mboss/guardian/p/sweep_e/s5_2
execute if score #gdSwEl mb matches 3 run function rlk:mboss/guardian/p/sweep_e/s5_3
execute if score #gdSwEl mb matches 4 run function rlk:mboss/guardian/p/sweep_e/s5_4
execute if score #gdSwEl mb matches 1 run playsound minecraft:block.fire.ambient hostile @a[tag=player] ~ ~ ~ 0.9 1 0.3
execute if score #gdSwEl mb matches 2 run playsound minecraft:entity.player.splash hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
execute if score #gdSwEl mb matches 3 run playsound minecraft:block.copper_bulb.turn_on hostile @a[tag=player] ~ ~ ~ 0.6 1.5 0.2
execute if score #gdSwEl mb matches 4 run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.7 1.8 0.23
