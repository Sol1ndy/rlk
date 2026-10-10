# 구역 건설 (boss7_2, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
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
fill 29 200 15 33 200 16 minecraft:deepslate
fill 34 200 -12 36 200 -9 minecraft:gravel
fill 28 200 9 32 200 11 minecraft:gravel
fill 41 200 4 42 200 5 minecraft:coarse_dirt
fill 29 200 -6 30 200 -3 minecraft:cobblestone
fill 47 200 -14 48 200 -13 minecraft:cobblestone
fill 47 200 11 49 200 12 minecraft:deepslate
fill 57 200 -5 58 200 -2 minecraft:coarse_dirt
fill 29 200 -13 32 200 -10 minecraft:coarse_dirt
fill 34 200 -2 36 200 -1 minecraft:coarse_dirt
fill 35 200 -3 37 200 0 minecraft:coarse_dirt
fill 20 205 -12 20 208 -11 minecraft:deepslate
fill 20 206 -7 20 207 -5 minecraft:deepslate
fill 20 204 -1 20 207 -1 minecraft:coal_ore
fill 29 203 -20 33 203 -20 minecraft:cobblestone
fill 34 202 -20 35 204 -20 minecraft:iron_ore
fill 21 204 -20 21 207 -20 minecraft:cobblestone
fill 39 206 -20 39 209 -20 minecraft:deepslate
fill 20 204 -20 22 205 -20 minecraft:coal_ore
fill 20 205 19 20 207 19 minecraft:spruce_planks
fill 20 205 4 20 207 8 minecraft:tuff
fill 20 207 10 20 209 15 minecraft:coal_ore
fill 20 203 14 20 203 17 minecraft:coal_ore
fill 20 209 16 20 209 16 minecraft:cobblestone
fill 20 206 0 20 207 1 minecraft:coal_ore
fill 25 205 19 26 208 19 minecraft:deepslate
fill 25 207 19 26 209 19 minecraft:cobblestone
fill 25 202 19 30 202 19 minecraft:iron_ore
fill 32 202 19 34 203 19 minecraft:cobblestone
fill 31 203 19 32 205 19 minecraft:tuff
fill 34 204 19 39 204 19 minecraft:tuff
fill 59 210 -19 59 210 -14 minecraft:cobblestone
fill 59 207 -15 59 208 -13 minecraft:tuff
fill 59 206 -8 59 206 -8 minecraft:coal_ore
fill 59 201 -20 59 202 -19 minecraft:spruce_planks
fill 59 205 -8 59 205 -5 minecraft:cobblestone
fill 54 201 -20 58 204 -20 minecraft:copper_ore
fill 50 208 -20 54 208 -20 minecraft:andesite
fill 49 207 -20 54 209 -20 minecraft:coal_ore
fill 50 203 -20 52 205 -20 minecraft:coal_ore
fill 54 204 -20 56 207 -20 minecraft:cobblestone
fill 46 207 -20 47 207 -20 minecraft:deepslate
fill 59 209 11 59 209 15 minecraft:iron_ore
fill 59 203 1 59 206 6 minecraft:coal_ore
fill 59 208 17 59 210 17 minecraft:iron_ore
fill 53 208 19 56 208 19 minecraft:spruce_planks
fill 43 206 19 46 207 19 minecraft:tuff
fill 46 209 19 46 210 19 minecraft:iron_ore
fill 50 205 19 50 206 19 minecraft:cobblestone
fill 20 210 -20 39 210 -1 minecraft:polished_deepslate
fill 21 210 -19 39 210 -1 minecraft:air
fill 20 210 0 39 210 19 minecraft:polished_deepslate
fill 21 210 0 39 210 18 minecraft:air
fill 40 210 -20 59 210 -1 minecraft:polished_deepslate
fill 40 210 -19 58 210 -1 minecraft:air
fill 40 210 0 59 210 19 minecraft:polished_deepslate
fill 40 210 0 58 210 18 minecraft:air
execute positioned 28 201 -16 run function rlk:room/prop/m_rail_x
execute positioned 38 201 10 run function rlk:room/prop/m_pebble
execute positioned 22 201 9 run function rlk:room/prop/m_pebble
execute positioned 25 201 3 run function rlk:room/prop/m_torch
execute positioned 47 201 9 run function rlk:room/prop/m_rail_z
execute positioned 36 201 3 run function rlk:room/prop/m_rail_x
execute positioned 29 201 2 run function rlk:room/prop/m_pebble
execute positioned 51 201 12 run function rlk:room/prop/m_pebble
execute positioned 28 201 -8 run function rlk:room/prop/m_rail_x
execute positioned 54 201 15 run function rlk:room/prop/m_rail_x
execute positioned 34 201 -11 run function rlk:room/prop/m_pebble
setblock 21 203 -9 minecraft:wall_torch[facing=east]
setblock 40 203 18 minecraft:wall_torch[facing=north]
setblock 29 203 -19 minecraft:wall_torch[facing=south]
setblock 58 203 9 minecraft:wall_torch[facing=west]
setblock 21 203 -8 minecraft:wall_torch[facing=east]
setblock 21 203 18 minecraft:wall_torch[facing=east]
setblock 45 203 -19 minecraft:wall_torch[facing=south]
setblock 21 203 17 minecraft:wall_torch[facing=east]
