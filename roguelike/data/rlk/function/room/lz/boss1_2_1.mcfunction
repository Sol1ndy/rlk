# 구역 건설 (boss1_2, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
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
fill -32 200 -28 -29 200 -26 minecraft:coarse_dirt
fill -19 200 -8 -17 200 -7 minecraft:coarse_dirt
fill -38 200 -12 -34 200 -9 minecraft:deepslate
fill -16 200 -21 -15 200 -18 minecraft:deepslate
fill -34 200 -6 -33 200 -4 minecraft:coarse_dirt
fill -25 200 -22 -24 200 -20 minecraft:deepslate
fill -35 200 -21 -32 200 -19 minecraft:coarse_dirt
fill -21 200 -18 -19 200 -15 minecraft:gravel
fill -16 200 -22 -13 200 -20 minecraft:deepslate
fill -17 200 -29 -16 200 -26 minecraft:cobblestone
fill -40 205 -36 -40 206 -36 minecraft:cobblestone
fill -40 201 -37 -40 203 -37 minecraft:cobblestone
fill -40 207 -32 -40 209 -30 minecraft:coal_ore
fill -24 204 -40 -22 206 -40 minecraft:tuff
fill -32 208 -40 -28 210 -40 minecraft:tuff
fill -40 207 -40 -36 207 -40 minecraft:cobblestone
fill -34 204 -40 -34 206 -40 minecraft:spruce_planks
fill -40 208 -3 -40 210 -1 minecraft:copper_ore
fill -40 201 -10 -40 204 -9 minecraft:tuff
fill -40 210 -9 -40 210 -9 minecraft:tuff
fill -40 202 -4 -40 205 -3 minecraft:cobblestone
fill -39 210 -1 -37 210 -1 minecraft:copper_ore
fill -34 209 -1 -30 210 -1 minecraft:coal_ore
fill -29 207 -1 -28 210 -1 minecraft:cobblestone
fill -26 210 -1 -23 210 -1 minecraft:coal_ore
fill -34 204 -1 -30 207 -1 minecraft:deepslate
fill -1 204 -31 -1 207 -30 minecraft:andesite
fill -1 209 -32 -1 210 -31 minecraft:copper_ore
fill -1 204 -36 -1 207 -32 minecraft:cobblestone
fill -7 210 -40 -2 210 -40 minecraft:andesite
fill -13 203 -40 -13 205 -40 minecraft:cobblestone
fill -15 203 -40 -11 204 -40 minecraft:andesite
fill -15 209 -40 -12 210 -40 minecraft:tuff
fill -5 206 -40 -5 209 -40 minecraft:coal_ore
fill -1 210 -7 -1 210 -7 minecraft:iron_ore
fill -1 201 -14 -1 204 -9 minecraft:iron_ore
fill -1 201 -14 -1 202 -11 minecraft:andesite
fill -1 201 -6 -1 201 -1 minecraft:cobblestone
fill -6 210 -1 -6 210 -1 minecraft:spruce_planks
fill -9 206 -1 -9 208 -1 minecraft:cobblestone
fill -4 201 -1 -3 201 -1 minecraft:andesite
fill -6 210 -1 -1 210 -1 minecraft:copper_ore
fill -40 210 -40 -21 210 -21 minecraft:polished_deepslate
fill -39 210 -39 -21 210 -21 minecraft:air
fill -40 210 -20 -21 210 -1 minecraft:polished_deepslate
fill -39 210 -20 -21 210 -2 minecraft:air
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -20 210 -39 -2 210 -21 minecraft:air
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -20 210 -20 -2 210 -2 minecraft:air
execute positioned -31 201 -28 run function rlk:room/prop/m_pebble
execute positioned -36 201 -20 run function rlk:room/prop/m_pebble
execute positioned -17 201 -25 run function rlk:room/prop/m_rail_x
execute positioned -26 201 -30 run function rlk:room/prop/m_rail_x
execute positioned -33 201 -6 run function rlk:room/prop/m_rail_z
execute positioned -18 201 -26 run function rlk:room/prop/m_rail_x
execute positioned -38 201 -34 run function rlk:room/prop/m_pebble
execute positioned -35 201 -17 run function rlk:room/prop/m_rail_z
execute positioned -33 201 -18 run function rlk:room/prop/m_pebble
execute positioned -37 201 -3 run function rlk:room/prop/m_pebble
execute positioned -18 201 -26 run function rlk:room/prop/m_rail_z
execute positioned -14 201 -10 run function rlk:room/prop/m_rail_x
setblock -39 203 -37 minecraft:wall_torch[facing=east]
setblock -2 203 -27 minecraft:wall_torch[facing=west]
setblock -39 203 -38 minecraft:wall_torch[facing=east]
setblock -39 203 -21 minecraft:wall_torch[facing=east]
setblock -29 203 -2 minecraft:wall_torch[facing=north]
setblock -24 203 -39 minecraft:wall_torch[facing=south]
setblock -39 203 -19 minecraft:wall_torch[facing=east]
setblock -2 203 -2 minecraft:wall_torch[facing=west]
