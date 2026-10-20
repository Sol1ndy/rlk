# meteor #azCT 72
kill @e[type=minecraft:item_display,tag=rlk_mb_az_p32p2,limit=1]
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p32m2,limit=1] run function rlk:mboss/azhdaha/fx/p/meteor_small {h:60}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p32m2,limit=1] run function rlk:mboss/azhdaha/fx/snd/meteor_fall
