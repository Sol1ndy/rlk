# Q6 feather 4 lands (@s = body): the burst at its spot, the feather and the spot marker gone.
execute at @e[type=minecraft:marker,tag=rlk_kn_fl4,limit=1] positioned ~ 201 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.6 0.2 0.6 0 16 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_fl4,limit=1] positioned ~ 201 ~ run particle minecraft:crimson_spore ~ ~ ~ 0.4 0.1 0.4 0.02 6 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_fl4,limit=1] run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.9 1 0.3
execute at @e[type=minecraft:marker,tag=rlk_kn_fl4,limit=1] run playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 0.6 0.6 0.2
kill @e[tag=rlk_kn_fth4]
kill @e[type=minecraft:marker,tag=rlk_kn_fl4]
