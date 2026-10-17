# Spear 2 (T0+80): it drops in 1 t (teleport_duration 1) and strikes; the hazard resolves this tick.
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p13d1]
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p13s1,limit=1] at @s run tp @s ~ ~-4.2 ~
execute if score #gp13K1 mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run function rlk:mboss/guardian/p/fail/hit1
execute if score #gp13K1 mb matches 2 at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run function rlk:mboss/guardian/p/fail/hit2
execute if score #gp13K1 mb matches 3 at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run function rlk:mboss/guardian/p/fail/hit3
execute if score #gp13K1 mb matches 4 at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run function rlk:mboss/guardian/p/fail/hit4
execute if score #gp13K1 mb matches 5 at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run function rlk:mboss/guardian/p/fail/hit5
execute if score #gp13K1 mb matches 6 at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run function rlk:mboss/guardian/p/fail/hit6
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run tp @e[type=minecraft:block_display,tag=rlk_mb_gd_p13fnew] ~ ~ ~ ~ 0
tag @e[type=minecraft:block_display,tag=rlk_mb_gd_p13fnew] add rlk_mb_gd_p13f1
tag @e[type=minecraft:block_display,tag=rlk_mb_gd_p13fnew] remove rlk_mb_gd_p13fnew
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run playsound minecraft:item.trident.hit_ground hostile @a[tag=player] ~ ~ ~ 1 0.5 0.3
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.6 0.8 0.3
