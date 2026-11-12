# spikes #azPT 76
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p4s] run particle minecraft:dust{color:[255f,196f,64f],scale:1.6} ~ ~1.1 ~ 0.25 0.7 0.25 0 4 force @a[tag=player]
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p4s] run particle minecraft:wax_on ~ ~1.2 ~ 0.3 0.6 0.3 0 2 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p4a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_p4a,limit=1] run function rlk:boss/azhdaha/p/spikes/burst0
