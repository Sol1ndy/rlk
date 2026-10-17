# Spear 2 drops in 1 t and strikes (the hazard resolves this tick).
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p13s1,limit=1] at @s run tp @s ~ ~-3.8 ~
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run function rlk:fx/nv/card {kind:"burst",pos:"~ ~1.4 ~",rot:"~ ~",bb:"center",roll:0,spin:20,s0:0.8,s1:3.4,move:"0f,0f,0f",life:6,fade:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run particle minecraft:dust{color:[1f,0.96f,0.75f],scale:1.8} ~ ~4 ~ 0.2 4 0.2 0 30 force @a[tag=player]
execute if score #gdFailK2 mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run particle minecraft:dust{color:[1f,0.541f,0.298f],scale:1.6} ~ ~0.6 ~ 1.8 0.4 1.8 0 30 force @a[tag=player]
execute if score #gdFailK2 mb matches 2 at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run particle minecraft:dust{color:[0.361f,0.784f,1f],scale:1.6} ~ ~0.6 ~ 1.8 0.4 1.8 0 30 force @a[tag=player]
execute if score #gdFailK2 mb matches 3 at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run particle minecraft:dust{color:[0.824f,0.51f,0.98f],scale:1.6} ~ ~0.6 ~ 1.8 0.4 1.8 0 30 force @a[tag=player]
execute if score #gdFailK2 mb matches 4 at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run particle minecraft:dust{color:[0.635f,0.996f,0.992f],scale:1.6} ~ ~0.6 ~ 1.8 0.4 1.8 0 30 force @a[tag=player]
execute if score #gdFailK2 mb matches 5 at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run particle minecraft:dust{color:[0.988f,0.898f,0.51f],scale:1.6} ~ ~0.6 ~ 1.8 0.4 1.8 0 30 force @a[tag=player]
execute if score #gdFailK2 mb matches 6 at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run particle minecraft:dust{color:[0.651f,0.808f,0.992f],scale:1.6} ~ ~0.6 ~ 1.8 0.4 1.8 0 30 force @a[tag=player]
playsound minecraft:item.trident.hit_ground hostile @a[tag=player] ~ ~ ~ 1 0.5 0.3
playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.6 0.8 0.3
playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.8 0.7 0.3
playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 1 0.8 0.3
