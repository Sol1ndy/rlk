# 구역 건설 (boss4_2, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -20 39 200 -1 minecraft:tuff
fill 20 201 -20 39 210 -1 minecraft:stone
fill 21 201 -19 39 210 -1 minecraft:air
fill 21 209 -19 39 209 -1 minecraft:light[level=15]
fill 20 200 0 39 200 19 minecraft:tuff
fill 20 201 0 39 210 19 minecraft:stone
fill 21 201 0 39 210 18 minecraft:air
fill 21 209 0 39 209 18 minecraft:light[level=15]
fill 40 200 -20 59 200 -1 minecraft:tuff
fill 40 201 -20 59 210 -1 minecraft:stone
fill 40 201 -19 58 210 -1 minecraft:air
fill 40 209 -19 58 209 -1 minecraft:light[level=15]
fill 40 200 0 59 200 19 minecraft:tuff
fill 40 201 0 59 210 19 minecraft:stone
fill 40 201 0 58 210 18 minecraft:air
fill 40 209 0 58 209 18 minecraft:light[level=15]
fill 56 200 -19 57 200 -16 minecraft:gravel
fill 42 200 1 43 200 2 minecraft:coarse_dirt
fill 49 200 5 50 200 7 minecraft:coarse_dirt
fill 39 200 -19 40 200 -17 minecraft:cobblestone
fill 52 200 -1 56 200 0 minecraft:gravel
fill 30 200 6 31 200 8 minecraft:coarse_dirt
fill 47 200 -11 49 200 -10 minecraft:gravel
fill 20 202 -9 20 202 -4 minecraft:iron_ore
fill 20 202 -6 20 205 -5 minecraft:tuff
fill 20 202 -14 20 205 -12 minecraft:spruce_planks
fill 20 207 -18 20 207 -15 minecraft:andesite
fill 29 208 -20 34 208 -20 minecraft:cobblestone
fill 33 203 -20 35 206 -20 minecraft:deepslate
fill 28 209 -20 32 210 -20 minecraft:cobblestone
fill 28 205 -20 28 205 -20 minecraft:cobblestone
fill 30 209 -20 32 210 -20 minecraft:andesite
fill 35 205 -20 36 208 -20 minecraft:tuff
fill 20 201 3 20 202 3 minecraft:copper_ore
fill 20 209 5 20 209 9 minecraft:cobblestone
fill 20 207 8 20 210 10 minecraft:andesite
fill 20 202 13 20 205 14 minecraft:cobblestone
fill 36 204 19 37 205 19 minecraft:deepslate
fill 38 204 19 39 205 19 minecraft:andesite
fill 35 205 19 35 206 19 minecraft:cobblestone
fill 59 206 -2 59 207 -2 minecraft:cobblestone
fill 59 201 -17 59 202 -16 minecraft:coal_ore
fill 59 205 -20 59 205 -15 minecraft:cobblestone
fill 59 205 -15 59 208 -13 minecraft:cobblestone
fill 59 203 -10 59 203 -9 minecraft:deepslate
fill 59 208 -10 59 210 -9 minecraft:spruce_planks
fill 44 201 -20 44 203 -20 minecraft:andesite
fill 54 203 -20 54 205 -20 minecraft:iron_ore
fill 42 202 -20 42 204 -20 minecraft:spruce_planks
fill 52 208 -20 56 208 -20 minecraft:deepslate
fill 57 210 -20 59 210 -20 minecraft:andesite
fill 59 205 3 59 205 8 minecraft:deepslate
fill 59 203 5 59 204 5 minecraft:coal_ore
fill 59 210 0 59 210 1 minecraft:cobblestone
fill 50 210 19 53 210 19 minecraft:andesite
fill 47 209 19 49 210 19 minecraft:copper_ore
fill 46 205 19 51 205 19 minecraft:copper_ore
fill 49 210 19 49 210 19 minecraft:iron_ore
fill 43 207 19 45 208 19 minecraft:deepslate
fill 40 201 19 40 201 19 minecraft:andesite
fill 20 210 -20 39 210 -1 minecraft:polished_deepslate
fill 21 210 -19 39 210 -1 minecraft:air
fill 20 210 0 39 210 19 minecraft:polished_deepslate
fill 21 210 0 39 210 18 minecraft:air
fill 40 210 -20 59 210 -1 minecraft:polished_deepslate
fill 40 210 -19 58 210 -1 minecraft:air
fill 40 210 0 59 210 19 minecraft:polished_deepslate
fill 40 210 0 58 210 18 minecraft:air
execute positioned 32 201 3 run function rlk:room/prop/m_pebble
execute positioned 56 201 -6 run function rlk:room/prop/m_pebble
execute positioned 44 201 18 run function rlk:room/prop/m_rail_x
execute positioned 57 201 13 run function rlk:room/prop/m_rail_x
execute positioned 45 201 -9 run function rlk:room/prop/m_pebble
execute positioned 34 201 1 run function rlk:room/prop/m_rail_z
execute positioned 29 201 8 run function rlk:room/prop/m_rail_x
execute positioned 52 201 -15 run function rlk:room/prop/m_rail_x
execute positioned 55 201 -15 run function rlk:room/prop/m_pebble
execute positioned 45 201 9 run function rlk:room/prop/m_pebble
setblock 47 203 -19 minecraft:wall_torch[facing=south]
setblock 21 203 8 minecraft:wall_torch[facing=east]
setblock 21 203 12 minecraft:wall_torch[facing=east]
setblock 21 203 -16 minecraft:wall_torch[facing=east]
setblock 54 203 -19 minecraft:wall_torch[facing=south]
setblock 49 203 18 minecraft:wall_torch[facing=north]
setblock 21 203 5 minecraft:wall_torch[facing=east]
setblock 21 203 10 minecraft:wall_torch[facing=east]
