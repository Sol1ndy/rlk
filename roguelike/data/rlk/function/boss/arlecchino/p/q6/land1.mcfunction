# Q6 feather 1 lands (@s = body): the burst at its spot, the feather and the spot marker gone.
execute at @e[type=minecraft:marker,tag=rlk_kn_fl1,limit=1] positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/p/feather_hit
execute at @e[type=minecraft:marker,tag=rlk_kn_fl1,limit=1] run function rlk:boss/arlecchino/fx/snd/impact
kill @e[tag=rlk_kn_fth1]
kill @e[type=minecraft:marker,tag=rlk_kn_fl1]
