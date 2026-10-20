# Seal stele 3 shatters into chunks.
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_seal_s3] positioned ~ ~-1.6 ~ run function rlk:mboss/azhdaha/fx/p/stele_shatter
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_seal_s3] run function rlk:mboss/azhdaha/fx/snd/stele_break
kill @e[type=minecraft:item_display,tag=rlk_mb_az_seal_s3]
