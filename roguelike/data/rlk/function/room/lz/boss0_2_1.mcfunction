# 구역 건설 (boss0_2, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -40 -21 200 -21 minecraft:tuff
fill -40 201 -40 -21 210 -21 minecraft:stone
fill -39 201 -39 -21 210 -21 minecraft:air
fill -39 209 -39 -21 209 -21 minecraft:light[level=15]
fill -40 200 -20 -21 200 -1 minecraft:tuff
fill -40 201 -20 -21 210 -1 minecraft:stone
fill -39 201 -20 -21 210 -2 minecraft:air
fill -39 209 -20 -21 209 -2 minecraft:light[level=15]
fill -20 200 -40 -1 200 -21 minecraft:tuff
fill -20 201 -40 -1 210 -21 minecraft:stone
fill -20 201 -39 -2 210 -21 minecraft:air
fill -20 209 -39 -2 209 -21 minecraft:light[level=15]
fill -20 200 -20 -1 200 -1 minecraft:tuff
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -20 201 -20 -2 210 -2 minecraft:air
fill -20 209 -20 -2 209 -2 minecraft:light[level=15]
fill -28 200 -10 -25 200 -8 minecraft:coarse_dirt
fill -24 200 -28 -23 200 -27 minecraft:deepslate
fill -8 200 -20 -6 200 -17 minecraft:deepslate
fill -7 200 -30 -4 200 -29 minecraft:gravel
fill -24 200 -7 -23 200 -4 minecraft:deepslate
fill -33 200 -29 -30 200 -27 minecraft:cobblestone
fill -21 200 -16 -19 200 -15 minecraft:coarse_dirt
fill -16 200 -18 -14 200 -16 minecraft:deepslate
fill -6 200 -20 -5 200 -17 minecraft:gravel
fill -25 200 -14 -24 200 -13 minecraft:deepslate
fill -35 200 -21 -33 200 -19 minecraft:gravel
fill -4 200 -10 -2 200 -8 minecraft:cobblestone
fill -5 200 -27 -3 200 -24 minecraft:coarse_dirt
fill -22 200 -9 -19 200 -8 minecraft:gravel
fill -40 204 -36 -40 207 -33 minecraft:spruce_planks
fill -40 204 -29 -40 207 -26 minecraft:andesite
fill -40 203 -33 -40 205 -32 minecraft:coal_ore
fill -32 205 -40 -31 207 -40 minecraft:andesite
fill -30 204 -40 -30 204 -40 minecraft:copper_ore
fill -35 201 -40 -30 202 -40 minecraft:tuff
fill -40 210 -18 -40 210 -13 minecraft:copper_ore
fill -40 204 -3 -40 205 -3 minecraft:coal_ore
fill -40 202 -16 -40 202 -11 minecraft:cobblestone
fill -40 208 -11 -40 208 -11 minecraft:tuff
fill -40 210 -7 -40 210 -5 minecraft:cobblestone
fill -40 206 -15 -40 206 -12 minecraft:deepslate
fill -36 208 -1 -36 208 -1 minecraft:andesite
fill -39 203 -1 -39 205 -1 minecraft:spruce_planks
fill -33 203 -1 -29 204 -1 minecraft:coal_ore
fill -1 203 -35 -1 203 -31 minecraft:tuff
fill -1 210 -23 -1 210 -22 minecraft:tuff
fill -1 210 -28 -1 210 -23 minecraft:cobblestone
fill -1 201 -24 -1 202 -21 minecraft:tuff
fill -1 206 -25 -1 208 -22 minecraft:deepslate
fill -12 208 -40 -9 210 -40 minecraft:cobblestone
fill -14 204 -40 -11 205 -40 minecraft:iron_ore
fill -10 207 -40 -8 209 -40 minecraft:andesite
fill -15 204 -40 -11 206 -40 minecraft:deepslate
fill -16 208 -40 -16 209 -40 minecraft:iron_ore
fill -1 204 -2 -1 205 -1 minecraft:deepslate
fill -1 201 -11 -1 202 -10 minecraft:andesite
fill -1 206 -19 -1 207 -16 minecraft:andesite
fill -1 205 -5 -1 205 -2 minecraft:deepslate
fill -1 207 -11 -1 210 -6 minecraft:tuff
fill -1 206 -5 -1 206 -5 minecraft:deepslate
fill -8 207 -1 -6 207 -1 minecraft:deepslate
fill -10 205 -1 -10 206 -1 minecraft:tuff
fill -16 210 -1 -15 210 -1 minecraft:copper_ore
fill -40 210 -40 -21 210 -21 minecraft:polished_deepslate
fill -39 210 -39 -21 210 -21 minecraft:air
fill -40 210 -20 -21 210 -1 minecraft:polished_deepslate
fill -39 210 -20 -21 210 -2 minecraft:air
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -20 210 -39 -2 210 -21 minecraft:air
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -20 210 -20 -2 210 -2 minecraft:air
execute positioned -9 201 -24 run function rlk:room/prop/m_pebble
execute positioned -6 201 -11 run function rlk:room/prop/m_rail_x
execute positioned -17 201 -11 run function rlk:room/prop/m_rail_z
execute positioned -39 201 -31 run function rlk:room/prop/m_pebble
execute positioned -28 201 -29 run function rlk:room/prop/m_rail_x
execute positioned -7 201 -19 run function rlk:room/prop/m_pebble
execute positioned -20 201 -27 run function rlk:room/prop/m_rail_x
execute positioned -8 201 -7 run function rlk:room/prop/m_torch
execute positioned -20 201 -25 run function rlk:room/prop/m_rail_z
execute positioned -7 201 -7 run function rlk:room/prop/m_rail_z
execute positioned -17 201 -38 run function rlk:room/prop/m_pebble
execute positioned -16 201 -16 run function rlk:room/prop/m_rail_z
execute positioned -9 201 -4 run function rlk:room/prop/m_pebble
setblock -30 203 -39 minecraft:wall_torch[facing=south]
setblock -26 203 -2 minecraft:wall_torch[facing=north]
setblock -6 203 -2 minecraft:wall_torch[facing=north]
setblock -32 203 -2 minecraft:wall_torch[facing=north]
setblock -39 203 -5 minecraft:wall_torch[facing=east]
setblock -2 203 -15 minecraft:wall_torch[facing=west]
setblock -39 203 -31 minecraft:wall_torch[facing=east]
setblock -2 203 -33 minecraft:wall_torch[facing=west]
