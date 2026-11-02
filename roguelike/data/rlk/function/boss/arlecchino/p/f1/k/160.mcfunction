# F1 pattern tick 160
scoreboard players set #bolw kn 1
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 8 3 8 0 200 force @a[tag=player]
execute at @s run playsound minecraft:entity.evoker_fangs.attack hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
execute at @s run playsound minecraft:entity.wither.shoot hostile @a[tag=player] ~ ~ ~ 0.5 0.6 0.17
