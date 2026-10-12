# Cancel the display and its parent together; the ring ends at frame58.
scoreboard players operation #rdVfxOwner rd = @s rdHId
execute as @e[type=minecraft:item_display,tag=rlk_rd_hvfx] if score @s rdVId = #rdVfxOwner rd run kill @s
kill @s
