# sweep_g clip tick 24
execute if entity @e[type=minecraft:marker,tag=rlk_mb_gd_p11h,scores={mbHzHit=1..}] run scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_gd_p11h] mbHzHit 1
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p11b1]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p11w3] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[0.82f,0.01f,0.04f]}}
function rlk:mboss/guardian/p/sweep_g/s4
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_q11c_0,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:10,transformation:{translation:[0.74f,1.219f,0.923f],left_rotation:[-0.071f,0.042f,0.852f,0.516f],scale:[0.017f,0.017f,0.017f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_q11c_5,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:12,transformation:{translation:[-0.722f,1.193f,-0.189f],left_rotation:[0.789f,0.049f,0.429f,-0.438f],scale:[0.024f,0.024f,0.024f],right_rotation:[0f,0f,0f,1f]}}
playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 0.5 1.2 0.3
