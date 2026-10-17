# sweep_g clip tick 16
execute if entity @e[type=minecraft:marker,tag=rlk_mb_gd_p11h,scores={mbHzHit=1..}] run scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_gd_p11h] mbHzHit 1
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p11w0] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[0.984f,0.01f,0.04f]}}
function rlk:mboss/guardian/p/sweep_g/s1
