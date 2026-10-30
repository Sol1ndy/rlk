# 구역 건설 (levelup0_2, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -20 39 200 -1 minecraft:tuff
fill 20 201 -20 39 210 -1 minecraft:stone
fill 21 201 -19 38 210 -2 minecraft:air
fill 21 209 -19 38 209 -2 minecraft:light[level=15]
fill 23 200 -10 26 200 -9 minecraft:deepslate
fill 20 209 -18 20 210 -17 minecraft:tuff
fill 20 205 -15 20 208 -10 minecraft:cobblestone
fill 20 205 -5 20 208 -3 minecraft:cobblestone
fill 20 201 -19 20 203 -14 minecraft:spruce_planks
fill 20 209 -8 20 209 -4 minecraft:copper_ore
fill 20 208 -11 20 210 -11 minecraft:tuff
fill 39 201 -14 39 201 -13 minecraft:cobblestone
fill 39 201 -12 39 203 -9 minecraft:spruce_planks
fill 27 205 -20 29 207 -20 minecraft:coal_ore
fill 36 206 -20 38 208 -20 minecraft:cobblestone
fill 27 206 -20 27 209 -20 minecraft:coal_ore
fill 38 205 -1 38 208 -1 minecraft:coal_ore
fill 34 204 -1 37 206 -1 minecraft:cobblestone
fill 30 201 -1 32 201 -1 minecraft:spruce_planks
fill 20 210 -20 39 210 -1 minecraft:polished_deepslate
fill 21 210 -19 38 210 -2 minecraft:air
fill 25 201 -19 33 201 -17 minecraft:tuff
fill 26 201 -16 32 201 -15 minecraft:tuff
execute positioned 37 201 -19 run function rlk:room/prop/m_crate_b
execute positioned 25 202 -19 run function rlk:room/prop/m_fence_x
execute positioned 35 201 -16 run function rlk:room/prop/m_pebble
execute positioned 36 201 -15 run function rlk:room/prop/m_pebble
execute positioned 30 201 -14 run function rlk:room/prop/m_rail_x
execute positioned 22 201 -5 run function rlk:room/prop/m_rail_x
setblock 36 203 -2 minecraft:wall_torch[facing=north]
setblock 34 203 -2 minecraft:wall_torch[facing=north]
