# Q0 stage dive tick 22
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] positioned ~ 201 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 4 0.3 4 0 40 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run playsound minecraft:block.pointed_dripstone.place hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run playsound minecraft:item.trident.return hostile @a[tag=player] ~ ~ ~ 0.5 0.6 0.17
