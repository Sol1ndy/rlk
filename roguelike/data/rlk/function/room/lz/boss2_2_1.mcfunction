# 구역 건설 (boss2_2, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 0 39 200 19 minecraft:tuff
fill 20 201 0 39 210 19 minecraft:stone
fill 21 201 1 39 210 19 minecraft:air
fill 21 209 1 39 209 19 minecraft:light[level=15]
fill 20 200 20 39 200 39 minecraft:tuff
fill 20 201 20 39 210 39 minecraft:stone
fill 21 201 20 39 210 38 minecraft:air
fill 21 209 20 39 209 38 minecraft:light[level=15]
fill 40 200 0 59 200 19 minecraft:tuff
fill 40 201 0 59 210 19 minecraft:stone
fill 40 201 1 58 210 19 minecraft:air
fill 40 209 1 58 209 19 minecraft:light[level=15]
fill 40 200 20 59 200 39 minecraft:tuff
fill 40 201 20 59 210 39 minecraft:stone
fill 40 201 20 58 210 38 minecraft:air
fill 40 209 20 58 209 38 minecraft:light[level=15]
fill 22 200 22 25 200 23 minecraft:coarse_dirt
fill 52 200 20 54 200 22 minecraft:deepslate
fill 41 200 19 43 200 22 minecraft:coarse_dirt
fill 48 200 26 49 200 27 minecraft:cobblestone
fill 23 200 17 27 200 18 minecraft:gravel
fill 39 200 6 41 200 7 minecraft:gravel
fill 20 210 9 20 210 10 minecraft:coal_ore
fill 20 209 13 20 210 18 minecraft:deepslate
fill 20 203 5 20 205 5 minecraft:coal_ore
fill 20 203 1 20 205 1 minecraft:tuff
fill 20 208 7 20 209 8 minecraft:iron_ore
fill 20 206 9 20 206 9 minecraft:deepslate
fill 29 208 0 30 210 0 minecraft:cobblestone
fill 20 207 0 21 208 0 minecraft:cobblestone
fill 25 206 0 29 206 0 minecraft:deepslate
fill 20 202 35 20 203 36 minecraft:andesite
fill 20 207 25 20 209 26 minecraft:deepslate
fill 20 205 33 20 207 35 minecraft:coal_ore
fill 20 210 23 20 210 24 minecraft:iron_ore
fill 27 208 39 31 210 39 minecraft:andesite
fill 36 202 39 38 205 39 minecraft:tuff
fill 31 207 39 34 208 39 minecraft:andesite
fill 28 209 39 31 210 39 minecraft:iron_ore
fill 34 206 39 38 208 39 minecraft:coal_ore
fill 30 210 39 34 210 39 minecraft:andesite
fill 59 210 4 59 210 5 minecraft:andesite
fill 59 206 7 59 209 8 minecraft:coal_ore
fill 59 205 10 59 207 12 minecraft:andesite
fill 42 206 0 47 208 0 minecraft:coal_ore
fill 49 207 0 51 209 0 minecraft:cobblestone
fill 45 210 0 48 210 0 minecraft:coal_ore
fill 49 205 0 53 206 0 minecraft:deepslate
fill 59 210 32 59 210 33 minecraft:cobblestone
fill 59 205 20 59 208 21 minecraft:deepslate
fill 59 206 36 59 208 39 minecraft:cobblestone
fill 59 205 32 59 206 34 minecraft:tuff
fill 59 209 24 59 210 29 minecraft:iron_ore
fill 49 203 39 53 206 39 minecraft:deepslate
fill 47 206 39 47 206 39 minecraft:spruce_planks
fill 51 209 39 55 210 39 minecraft:andesite
fill 20 210 0 39 210 19 minecraft:polished_deepslate
fill 21 210 1 39 210 19 minecraft:air
fill 20 210 20 39 210 39 minecraft:polished_deepslate
fill 21 210 20 39 210 38 minecraft:air
fill 40 210 0 59 210 19 minecraft:polished_deepslate
fill 40 210 1 58 210 19 minecraft:air
fill 40 210 20 59 210 39 minecraft:polished_deepslate
fill 40 210 20 58 210 38 minecraft:air
execute positioned 24 201 23 run function rlk:room/prop/m_rail_x
execute positioned 27 201 37 run function rlk:room/prop/m_pebble
execute positioned 39 201 1 run function rlk:room/prop/m_pebble
execute positioned 27 201 33 run function rlk:room/prop/m_rail_x
execute positioned 44 201 10 run function rlk:room/prop/m_rail_x
execute positioned 44 201 10 run function rlk:room/prop/m_pebble
execute positioned 39 201 4 run function rlk:room/prop/m_rail_x
execute positioned 55 201 2 run function rlk:room/prop/m_pebble
execute positioned 56 201 11 run function rlk:room/prop/m_pebble
execute positioned 21 201 18 run function rlk:room/prop/m_pebble
execute positioned 39 201 6 run function rlk:room/prop/m_pebble
execute positioned 23 201 33 run function rlk:room/prop/m_rail_z
execute positioned 54 201 18 run function rlk:room/prop/m_rail_z
execute positioned 22 201 16 run function rlk:room/prop/m_pebble
setblock 30 203 1 minecraft:wall_torch[facing=south]
setblock 58 203 20 minecraft:wall_torch[facing=west]
setblock 58 203 25 minecraft:wall_torch[facing=west]
setblock 21 203 3 minecraft:wall_torch[facing=east]
setblock 39 203 38 minecraft:wall_torch[facing=north]
setblock 58 203 36 minecraft:wall_torch[facing=west]
setblock 21 203 22 minecraft:wall_torch[facing=east]
setblock 40 203 38 minecraft:wall_torch[facing=north]
