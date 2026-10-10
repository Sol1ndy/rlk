# 구역 건설 (boss6_2, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -40 19 200 -21 minecraft:tuff
fill 0 201 -40 19 210 -21 minecraft:stone
fill 1 201 -39 19 210 -21 minecraft:air
fill 1 209 -39 19 209 -21 minecraft:light[level=15]
fill 0 200 -20 19 200 -1 minecraft:tuff
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -20 19 210 -2 minecraft:air
fill 1 209 -20 19 209 -2 minecraft:light[level=15]
fill 20 200 -40 39 200 -21 minecraft:tuff
fill 20 201 -40 39 210 -21 minecraft:stone
fill 20 201 -39 38 210 -21 minecraft:air
fill 20 209 -39 38 209 -21 minecraft:light[level=15]
fill 20 200 -20 39 200 -1 minecraft:tuff
fill 20 201 -20 39 210 -1 minecraft:stone
fill 20 201 -20 38 210 -2 minecraft:air
fill 20 209 -20 38 209 -2 minecraft:light[level=15]
fill 7 200 -15 11 200 -14 minecraft:deepslate
fill 14 200 -12 15 200 -9 minecraft:cobblestone
fill 7 200 -13 8 200 -11 minecraft:gravel
fill 13 200 -32 17 200 -30 minecraft:cobblestone
fill 29 200 -10 33 200 -7 minecraft:gravel
fill 6 200 -36 10 200 -35 minecraft:deepslate
fill 31 200 -3 33 200 -2 minecraft:deepslate
fill 6 200 -11 8 200 -8 minecraft:coarse_dirt
fill 3 200 -18 4 200 -15 minecraft:deepslate
fill 0 205 -21 0 207 -21 minecraft:coal_ore
fill 0 207 -24 0 207 -24 minecraft:deepslate
fill 0 208 -37 0 208 -34 minecraft:cobblestone
fill 0 204 -28 0 204 -25 minecraft:tuff
fill 0 210 -28 0 210 -24 minecraft:iron_ore
fill 2 203 -40 6 205 -40 minecraft:spruce_planks
fill 17 203 -40 17 205 -40 minecraft:coal_ore
fill 14 206 -40 19 209 -40 minecraft:coal_ore
fill 4 209 -40 5 209 -40 minecraft:cobblestone
fill 7 206 -40 9 207 -40 minecraft:coal_ore
fill 7 208 -40 12 208 -40 minecraft:cobblestone
fill 0 206 -9 0 207 -9 minecraft:copper_ore
fill 0 209 -18 0 210 -13 minecraft:tuff
fill 0 209 -6 0 210 -1 minecraft:deepslate
fill 0 206 -15 0 207 -14 minecraft:andesite
fill 0 202 -4 0 202 -1 minecraft:andesite
fill 0 204 -1 2 207 -1 minecraft:cobblestone
fill 13 207 -1 17 208 -1 minecraft:copper_ore
fill 5 209 -1 10 210 -1 minecraft:spruce_planks
fill 39 207 -33 39 210 -28 minecraft:coal_ore
fill 39 209 -35 39 210 -34 minecraft:andesite
fill 39 210 -40 39 210 -38 minecraft:coal_ore
fill 39 208 -31 39 210 -28 minecraft:coal_ore
fill 39 209 -37 39 210 -32 minecraft:deepslate
fill 39 209 -26 39 210 -21 minecraft:cobblestone
fill 30 201 -40 34 201 -40 minecraft:tuff
fill 36 209 -40 36 210 -40 minecraft:deepslate
fill 33 201 -40 37 203 -40 minecraft:tuff
fill 35 203 -40 39 204 -40 minecraft:deepslate
fill 24 206 -40 25 207 -40 minecraft:copper_ore
fill 39 202 -13 39 202 -8 minecraft:andesite
fill 39 204 -13 39 205 -8 minecraft:iron_ore
fill 39 210 -12 39 210 -12 minecraft:deepslate
fill 27 203 -1 30 206 -1 minecraft:andesite
fill 27 207 -1 29 208 -1 minecraft:andesite
fill 36 201 -1 37 201 -1 minecraft:cobblestone
fill 26 201 -1 30 201 -1 minecraft:tuff
fill 0 210 -40 19 210 -21 minecraft:polished_deepslate
fill 1 210 -39 19 210 -21 minecraft:air
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -20 19 210 -2 minecraft:air
fill 20 210 -40 39 210 -21 minecraft:polished_deepslate
fill 20 210 -39 38 210 -21 minecraft:air
fill 20 210 -20 39 210 -1 minecraft:polished_deepslate
fill 20 210 -20 38 210 -2 minecraft:air
execute positioned 22 201 -6 run function rlk:room/prop/m_rail_x
execute positioned 31 201 -25 run function rlk:room/prop/m_rail_x
execute positioned 21 201 -15 run function rlk:room/prop/m_rail_z
execute positioned 1 201 -35 run function rlk:room/prop/m_rail_x
execute positioned 20 201 -39 run function rlk:room/prop/m_pebble
execute positioned 25 201 -15 run function rlk:room/prop/m_rail_x
execute positioned 30 201 -3 run function rlk:room/prop/m_torch
execute positioned 9 201 -4 run function rlk:room/prop/m_rail_z
execute positioned 19 201 -4 run function rlk:room/prop/m_rail_x
execute positioned 21 201 -26 run function rlk:room/prop/m_rail_z
execute positioned 27 201 -39 run function rlk:room/prop/m_pebble
execute positioned 13 201 -38 run function rlk:room/prop/m_rail_z
setblock 35 203 -2 minecraft:wall_torch[facing=north]
setblock 38 203 -38 minecraft:wall_torch[facing=west]
setblock 1 203 -20 minecraft:wall_torch[facing=east]
setblock 1 203 -12 minecraft:wall_torch[facing=east]
setblock 1 203 -22 minecraft:wall_torch[facing=east]
setblock 1 203 -28 minecraft:wall_torch[facing=east]
setblock 32 203 -39 minecraft:wall_torch[facing=south]
setblock 1 203 -39 minecraft:wall_torch[facing=south]
