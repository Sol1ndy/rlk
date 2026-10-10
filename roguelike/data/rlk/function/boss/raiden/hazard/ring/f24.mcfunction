# Exact ring radius 14.387097; visible band half-width0.7.
scoreboard players operation #rdVfxOwner rd = @s rdHId
execute as @e[type=minecraft:item_display,tag=rlk_rd_hvfx] if score @s rdVId = #rdVfxOwner rd run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_hazard/ring_24"
