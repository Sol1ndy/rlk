# meteor #azCT 60
kill @e[type=minecraft:item_display,tag=rlk_mb_az_p32p0,limit=1]
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p32m0,limit=1] run function rlk:mboss/azhdaha/fx/p/meteor_small {h:60}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p32m0,limit=1] run function rlk:mboss/azhdaha/fx/snd/meteor_fall
