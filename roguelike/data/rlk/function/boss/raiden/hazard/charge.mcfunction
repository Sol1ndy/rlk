# Four ticks before impact: charged borders, no full-path strike yet.
scoreboard players operation #rdVfxOwner rd = @s rdHId
scoreboard players set #rdChargeFrame rd 0
execute if score #rdUntil rd matches 1..2 run scoreboard players set #rdChargeFrame rd 1
execute as @e[type=minecraft:item_display,tag=rlk_rd_hvfx] if score @s rdVId = #rdVfxOwner rd run function rlk:boss/raiden/hazard/vfx_charge
