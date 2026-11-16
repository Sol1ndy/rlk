# The seal shatters: the prism breaks with a white flash; the glyph circle goes with it.
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_seal_prism] run function rlk:boss/azhdaha/fx/p/prism_shatter
function rlk:boss/azhdaha/fx/snd/seal_shatter
function rlk:boss/azhdaha/fx/hud/flash_white
function rlk:boss/azhdaha/rig/glow/gold_off
kill @e[type=minecraft:item_display,tag=rlk_mb_az_seal_prism]
