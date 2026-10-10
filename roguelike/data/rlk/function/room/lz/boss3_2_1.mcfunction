# 구역 건설 (boss3_2, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
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
fill 12 200 -16 13 200 -13 minecraft:gravel
fill 32 200 -33 34 200 -30 minecraft:gravel
fill 34 200 -28 35 200 -27 minecraft:cobblestone
fill 3 200 -34 7 200 -31 minecraft:coarse_dirt
fill 31 200 -23 33 200 -22 minecraft:coarse_dirt
fill 11 200 -23 13 200 -21 minecraft:gravel
fill 20 200 -7 22 200 -5 minecraft:deepslate
fill 0 209 -40 0 210 -36 minecraft:andesite
fill 0 204 -34 0 206 -29 minecraft:tuff
fill 0 201 -29 0 202 -27 minecraft:spruce_planks
fill 0 210 -34 0 210 -29 minecraft:deepslate
fill 4 210 -40 4 210 -40 minecraft:cobblestone
fill 2 209 -40 7 210 -40 minecraft:cobblestone
fill 10 209 -40 15 209 -40 minecraft:copper_ore
fill 0 201 -7 0 202 -5 minecraft:coal_ore
fill 0 210 -7 0 210 -3 minecraft:andesite
fill 0 202 -20 0 203 -17 minecraft:tuff
fill 0 203 -11 0 204 -7 minecraft:andesite
fill 0 204 -16 0 206 -11 minecraft:andesite
fill 0 202 -9 0 204 -5 minecraft:tuff
fill 12 207 -1 14 208 -1 minecraft:andesite
fill 0 210 -1 2 210 -1 minecraft:deepslate
fill 10 206 -1 11 206 -1 minecraft:andesite
fill 2 210 -1 3 210 -1 minecraft:cobblestone
fill 10 203 -1 15 205 -1 minecraft:iron_ore
fill 1 204 -1 1 207 -1 minecraft:deepslate
fill 39 204 -25 39 204 -23 minecraft:iron_ore
fill 39 202 -40 39 204 -40 minecraft:cobblestone
fill 39 207 -37 39 209 -35 minecraft:coal_ore
fill 39 206 -28 39 207 -23 minecraft:tuff
fill 39 203 -30 39 203 -29 minecraft:tuff
fill 34 210 -40 35 210 -40 minecraft:coal_ore
fill 23 210 -40 26 210 -40 minecraft:cobblestone
fill 35 206 -40 39 208 -40 minecraft:spruce_planks
fill 33 208 -40 38 210 -40 minecraft:tuff
fill 39 207 -8 39 210 -7 minecraft:cobblestone
fill 39 209 -13 39 210 -13 minecraft:tuff
fill 39 210 -17 39 210 -16 minecraft:copper_ore
fill 39 206 -13 39 206 -12 minecraft:iron_ore
fill 29 202 -1 33 202 -1 minecraft:copper_ore
fill 30 204 -1 35 205 -1 minecraft:coal_ore
fill 38 207 -1 38 207 -1 minecraft:iron_ore
fill 34 201 -1 38 204 -1 minecraft:cobblestone
fill 34 202 -1 34 205 -1 minecraft:deepslate
fill 0 210 -40 19 210 -21 minecraft:polished_deepslate
fill 1 210 -39 19 210 -21 minecraft:air
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -20 19 210 -2 minecraft:air
fill 20 210 -40 39 210 -21 minecraft:polished_deepslate
fill 20 210 -39 38 210 -21 minecraft:air
fill 20 210 -20 39 210 -1 minecraft:polished_deepslate
fill 20 210 -20 38 210 -2 minecraft:air
execute positioned 12 201 -23 run function rlk:room/prop/m_rail_z
execute positioned 27 201 -7 run function rlk:room/prop/m_rail_z
execute positioned 7 201 -27 run function rlk:room/prop/m_rail_z
execute positioned 8 201 -29 run function rlk:room/prop/m_rail_x
execute positioned 33 201 -7 run function rlk:room/prop/m_rail_x
execute positioned 6 201 -12 run function rlk:room/prop/m_rail_x
execute positioned 18 201 -25 run function rlk:room/prop/m_pebble
execute positioned 4 201 -37 run function rlk:room/prop/m_rail_x
execute positioned 25 201 -24 run function rlk:room/prop/m_rail_z
execute positioned 21 201 -12 run function rlk:room/prop/m_rail_z
execute positioned 18 201 -16 run function rlk:room/prop/m_pebble
execute positioned 21 201 -34 run function rlk:room/prop/m_rail_x
setblock 31 203 -2 minecraft:wall_torch[facing=north]
setblock 1 203 -36 minecraft:wall_torch[facing=east]
setblock 38 203 -20 minecraft:wall_torch[facing=west]
setblock 38 203 -8 minecraft:wall_torch[facing=west]
setblock 38 203 -31 minecraft:wall_torch[facing=west]
setblock 14 203 -39 minecraft:wall_torch[facing=south]
setblock 1 203 -31 minecraft:wall_torch[facing=east]
setblock 1 203 -22 minecraft:wall_torch[facing=east]
