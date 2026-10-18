# @s = crescent 2 on its landing tick: armed for this tick's pj step (the splash r 1.2 on the floor), the fire
# splash and the landing crack at its marker (gone with it).
scoreboard players set @s mbPjD 50
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12t2,limit=1] run function rlk:mboss/butterfly/fx/p/fire_land
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12t2,limit=1] run particle minecraft:dust{color:[0.345f,0.333f,0.259f],scale:1.6} ~ ~0.1 ~ 0.5 0.02 0.5 0 6 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12t2,limit=1] run function rlk:mboss/butterfly/fx/snd/fire_cres_land
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12t2]
