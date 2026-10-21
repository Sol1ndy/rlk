# meteor #azCT 84
kill @e[type=minecraft:item_display,tag=rlk_mb_az_p32p4,limit=1]
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p32m4,limit=1] run function rlk:boss/azhdaha/fx/p/meteor_small {h:60}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p32m4,limit=1] run function rlk:boss/azhdaha/fx/snd/meteor_fall
