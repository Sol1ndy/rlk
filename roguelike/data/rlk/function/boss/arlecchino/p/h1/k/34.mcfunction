# H1 pattern tick 34
scoreboard players set #bolw kn 1
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.9 0.33
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run playsound minecraft:entity.wither.shoot hostile @a[tag=player] ~ ~ ~ 0.3 1.6 0.1
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run particle minecraft:explosion ~ ~ ~ 0.5 0.1 0.5 0 2 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.8 0.2 0.8 0 24 force @a[tag=player]
