# 구역 건설 (boss5_2, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 0 -41 200 19 minecraft:tuff
fill -60 201 0 -41 210 19 minecraft:stone
fill -59 201 1 -41 210 19 minecraft:air
fill -59 209 1 -41 209 19 minecraft:light[level=15]
fill -60 200 20 -41 200 39 minecraft:tuff
fill -60 201 20 -41 210 39 minecraft:stone
fill -59 201 20 -41 210 38 minecraft:air
fill -59 209 20 -41 209 38 minecraft:light[level=15]
fill -40 200 0 -21 200 19 minecraft:tuff
fill -40 201 0 -21 210 19 minecraft:stone
fill -40 201 1 -22 210 19 minecraft:air
fill -40 209 1 -22 209 19 minecraft:light[level=15]
fill -40 200 20 -21 200 39 minecraft:tuff
fill -40 201 20 -21 210 39 minecraft:stone
fill -40 201 20 -22 210 38 minecraft:air
fill -40 209 20 -22 209 38 minecraft:light[level=15]
fill -29 200 21 -28 200 22 minecraft:gravel
fill -46 200 24 -45 200 26 minecraft:gravel
fill -38 200 3 -37 200 5 minecraft:cobblestone
fill -52 200 36 -51 200 37 minecraft:deepslate
fill -27 200 37 -26 200 38 minecraft:gravel
fill -34 200 6 -32 200 7 minecraft:cobblestone
fill -56 200 33 -55 200 36 minecraft:deepslate
fill -59 200 37 -56 200 38 minecraft:coarse_dirt
fill -38 200 15 -35 200 16 minecraft:gravel
fill -38 200 28 -34 200 31 minecraft:coarse_dirt
fill -35 200 9 -32 200 12 minecraft:gravel
fill -60 203 14 -60 204 18 minecraft:iron_ore
fill -60 202 1 -60 203 4 minecraft:deepslate
fill -60 209 0 -60 209 3 minecraft:andesite
fill -60 204 3 -60 205 4 minecraft:copper_ore
fill -60 205 8 -60 205 8 minecraft:spruce_planks
fill -47 208 0 -42 210 0 minecraft:spruce_planks
fill -58 204 0 -53 204 0 minecraft:tuff
fill -53 202 0 -53 203 0 minecraft:cobblestone
fill -44 204 0 -42 206 0 minecraft:cobblestone
fill -57 205 0 -54 208 0 minecraft:tuff
fill -60 201 27 -60 204 29 minecraft:copper_ore
fill -60 206 25 -60 206 30 minecraft:iron_ore
fill -60 207 25 -60 208 25 minecraft:cobblestone
fill -60 202 27 -60 204 32 minecraft:deepslate
fill -60 205 31 -60 208 35 minecraft:andesite
fill -60 204 31 -60 205 33 minecraft:tuff
fill -44 208 39 -42 208 39 minecraft:deepslate
fill -60 206 39 -55 209 39 minecraft:tuff
fill -46 202 39 -43 203 39 minecraft:deepslate
fill -45 202 39 -45 202 39 minecraft:cobblestone
fill -49 204 39 -45 207 39 minecraft:coal_ore
fill -21 201 4 -21 202 7 minecraft:copper_ore
fill -21 206 1 -21 209 1 minecraft:andesite
fill -21 206 6 -21 208 11 minecraft:coal_ore
fill -21 210 0 -21 210 1 minecraft:andesite
fill -36 208 0 -31 210 0 minecraft:iron_ore
fill -25 201 0 -23 204 0 minecraft:tuff
fill -33 203 0 -32 203 0 minecraft:copper_ore
fill -21 201 22 -21 204 23 minecraft:deepslate
fill -21 208 29 -21 210 34 minecraft:coal_ore
fill -21 201 22 -21 201 22 minecraft:copper_ore
fill -21 206 24 -21 208 28 minecraft:deepslate
fill -21 207 38 -21 210 38 minecraft:coal_ore
fill -37 202 39 -35 204 39 minecraft:spruce_planks
fill -38 203 39 -34 206 39 minecraft:andesite
fill -22 202 39 -22 205 39 minecraft:andesite
fill -30 202 39 -26 204 39 minecraft:copper_ore
fill -37 205 39 -34 207 39 minecraft:deepslate
fill -60 210 0 -41 210 19 minecraft:polished_deepslate
fill -59 210 1 -41 210 19 minecraft:air
fill -60 210 20 -41 210 39 minecraft:polished_deepslate
fill -59 210 20 -41 210 38 minecraft:air
fill -40 210 0 -21 210 19 minecraft:polished_deepslate
fill -40 210 1 -22 210 19 minecraft:air
fill -40 210 20 -21 210 39 minecraft:polished_deepslate
fill -40 210 20 -22 210 38 minecraft:air
execute positioned -47 201 19 run function rlk:room/prop/m_rail_z
execute positioned -48 201 24 run function rlk:room/prop/m_rail_z
execute positioned -40 201 12 run function rlk:room/prop/m_rail_z
execute positioned -47 201 32 run function rlk:room/prop/m_rail_z
execute positioned -53 201 30 run function rlk:room/prop/m_pebble
execute positioned -30 201 2 run function rlk:room/prop/m_rail_z
execute positioned -58 201 29 run function rlk:room/prop/m_rail_x
execute positioned -33 201 11 run function rlk:room/prop/m_pebble
execute positioned -33 201 33 run function rlk:room/prop/m_rail_z
execute positioned -45 201 38 run function rlk:room/prop/m_pebble
execute positioned -38 201 27 run function rlk:room/prop/m_pebble
execute positioned -55 201 32 run function rlk:room/prop/m_pebble
execute positioned -33 201 6 run function rlk:room/prop/m_rail_z
setblock -59 203 22 minecraft:wall_torch[facing=east]
setblock -49 203 1 minecraft:wall_torch[facing=south]
setblock -59 203 13 minecraft:wall_torch[facing=east]
setblock -22 203 32 minecraft:wall_torch[facing=west]
setblock -25 203 1 minecraft:wall_torch[facing=south]
setblock -37 203 1 minecraft:wall_torch[facing=south]
setblock -59 203 31 minecraft:wall_torch[facing=east]
setblock -32 203 38 minecraft:wall_torch[facing=north]
