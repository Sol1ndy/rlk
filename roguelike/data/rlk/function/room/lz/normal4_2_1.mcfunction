# 구역 건설 (normal4_2, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 0 -21 200 19 minecraft:tuff
fill -40 201 0 -21 210 19 minecraft:stone
fill -39 201 1 -22 210 18 minecraft:air
fill -39 209 1 -22 209 18 minecraft:light[level=15]
fill -33 200 12 -30 200 14 minecraft:coarse_dirt
fill -29 200 11 -27 200 14 minecraft:cobblestone
fill -40 206 6 -40 207 7 minecraft:deepslate
fill -40 207 8 -40 207 13 minecraft:coal_ore
fill -40 201 12 -40 201 17 minecraft:andesite
fill -40 208 10 -40 209 14 minecraft:deepslate
fill -40 210 2 -40 210 5 minecraft:cobblestone
fill -21 201 4 -21 203 7 minecraft:copper_ore
fill -21 201 4 -21 203 9 minecraft:cobblestone
fill -21 208 4 -21 209 7 minecraft:andesite
fill -21 205 9 -21 206 12 minecraft:copper_ore
fill -21 210 2 -21 210 5 minecraft:cobblestone
fill -21 207 12 -21 210 14 minecraft:cobblestone
fill -26 207 0 -24 209 0 minecraft:copper_ore
fill -26 207 0 -24 207 0 minecraft:deepslate
fill -32 204 0 -27 204 0 minecraft:andesite
fill -33 204 19 -31 205 19 minecraft:andesite
fill -30 208 19 -28 210 19 minecraft:spruce_planks
fill -31 208 19 -27 209 19 minecraft:deepslate
fill -40 210 0 -21 210 19 minecraft:polished_deepslate
fill -39 210 1 -22 210 18 minecraft:air
fill -27 201 1 -27 201 3 minecraft:tuff
fill -26 201 3 -22 201 3 minecraft:tuff
fill -26 201 1 -22 201 2 minecraft:cobbled_deepslate
fill -26 202 1 -22 202 2 minecraft:tuff
execute positioned -26 202 3 run function rlk:room/prop/m_pillar_a
execute positioned -32 201 1 run function rlk:room/prop/m_crate_b
execute positioned -22 201 5 run function rlk:room/prop/m_pebble
execute positioned -36 201 2 run function rlk:room/prop/m_rail_x
execute positioned -38 201 12 run function rlk:room/prop/m_pebble
setblock -22 203 18 minecraft:wall_torch[facing=west]
setblock -33 203 18 minecraft:wall_torch[facing=north]
