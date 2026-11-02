# Q6 the impact (@s = body): the landing burst, every orb bursts.
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] positioned ~ 201 ~ run particle minecraft:explosion ~ ~ ~ 1 0.1 1 0 2 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] positioned ~ 201 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.6 0.2 1.6 0 24 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run playsound minecraft:block.anvil.land hostile @a[tag=player] ~ ~ ~ 0.5 0.5 0.17
execute as @e[tag=rlk_kn_p_q6,tag=rlk_kn_q6o] at @s positioned ~ 201 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 2 0.6 2 0 50 force @a[tag=player]
execute as @e[tag=rlk_kn_p_q6,tag=rlk_kn_q6o] at @s positioned ~ 201 ~ run particle minecraft:explosion ~ ~ ~ 1 0.2 1 0 1 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.9 0.9 0.3
kill @e[tag=rlk_kn_p_q6,tag=rlk_kn_q6o]
