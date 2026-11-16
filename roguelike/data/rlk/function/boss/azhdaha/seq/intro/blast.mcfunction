# The blast: a push-only ring r 8 (no damage) with its dome; the remaining steles crumble.
function rlk:mboss/push/ring {r:80,to:85,kb:4}
function rlk:boss/azhdaha/fx/p/shock_dome {r:80}
function rlk:boss/azhdaha/fx/snd/roar_ring
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_seal] at @s positioned ~ ~-1.6 ~ run function rlk:boss/azhdaha/fx/p/stele_shatter
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_seal,limit=1] run function rlk:boss/azhdaha/fx/snd/stele_break
kill @e[type=minecraft:item_display,tag=rlk_mb_az_seal]
