# The two arrival glyphs: upper = the tail element, lower = the leg element (kit glyph props).
execute if score #azTail mb matches 3 as @e[type=minecraft:item_display,tag=rlk_mb_az_ap_glyph_upper] run function rlk:boss/azhdaha/fx/prop/glyph/3
execute if score #azTail mb matches 4 as @e[type=minecraft:item_display,tag=rlk_mb_az_ap_glyph_upper] run function rlk:boss/azhdaha/fx/prop/glyph/4
execute if score #azLeg mb matches 1 as @e[type=minecraft:item_display,tag=rlk_mb_az_ap_glyph_lower] run function rlk:boss/azhdaha/fx/prop/glyph/1
execute if score #azLeg mb matches 2 as @e[type=minecraft:item_display,tag=rlk_mb_az_ap_glyph_lower] run function rlk:boss/azhdaha/fx/prop/glyph/2
