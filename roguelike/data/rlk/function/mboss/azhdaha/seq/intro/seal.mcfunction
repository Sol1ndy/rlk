# The seal shatters: the prism breaks with a white flash.
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_seal_prism] run function rlk:mboss/azhdaha/kstub/p/prism_shatter
function rlk:mboss/azhdaha/kstub/snd/seal_shatter
function rlk:mboss/azhdaha/kstub/hud/flash_white
kill @e[type=minecraft:item_display,tag=rlk_mb_az_seal_prism]
