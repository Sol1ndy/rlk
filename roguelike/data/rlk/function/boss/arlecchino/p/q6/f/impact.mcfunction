# Q6 the impact (@s = body): the landing burst, every orb bursts.
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/p/impact_burst {r:40,c:2}
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run function rlk:boss/arlecchino/fx/snd/fall_impact
execute as @e[tag=rlk_kn_p_q6,tag=rlk_kn_q6o] at @s positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/p/orb_burst {r:50}
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:boss/arlecchino/fx/snd/orb_burst
kill @e[tag=rlk_kn_p_q6,tag=rlk_kn_q6o]
