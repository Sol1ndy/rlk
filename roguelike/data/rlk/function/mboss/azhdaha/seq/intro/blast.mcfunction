# The blast: a push-only ring r 8 (no damage); the remaining steles crumble.
function rlk:mboss/push/ring {r:80,to:85,kb:4}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_seal] at @s run function rlk:mboss/azhdaha/kstub/p/stele_shatter
kill @e[type=minecraft:item_display,tag=rlk_mb_az_seal]
