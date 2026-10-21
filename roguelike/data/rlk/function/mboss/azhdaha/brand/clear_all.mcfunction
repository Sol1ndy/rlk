# Every brand and shard (death, abort, cleanup, uninstall, fight end; any executor).
execute as @a[tag=player] run function rlk:mboss/azhdaha/brand/clear
kill @e[type=minecraft:item_display,tag=rlk_az_shard]
data remove storage rlk:mboss az.hud.br
