# Q6 feather 3 lands (@s = body): the burst at its spot, the feather and the spot marker gone.
execute at @e[type=minecraft:marker,tag=rlk_kn_fl3,limit=1] positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/p/feather_hit
execute at @e[type=minecraft:marker,tag=rlk_kn_fl3,limit=1] run function rlk:boss/arlecchino/fx/snd/impact
kill @e[tag=rlk_kn_fth3]
kill @e[type=minecraft:marker,tag=rlk_kn_fl3]
