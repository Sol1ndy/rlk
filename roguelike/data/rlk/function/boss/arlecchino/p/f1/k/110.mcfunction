# F1 pattern tick 110
execute at @s run playsound minecraft:block.respawn_anchor.deplete hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.27
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
