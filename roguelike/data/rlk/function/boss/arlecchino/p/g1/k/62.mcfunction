# G1 pattern tick 62
scoreboard players set #bolw kn 1
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run playsound minecraft:entity.evoker_fangs.attack hostile @a[tag=player] ~ ~ ~ 1 1 0.33
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.27
execute as @e[type=minecraft:item_display,tag=rlk_kn_blade,tag=rlk_kn_p_g1] at @s run execute positioned ~ ~1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.6 1 0.6 0 20 force @a[tag=player]
