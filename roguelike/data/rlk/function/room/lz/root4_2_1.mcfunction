# 구역 건설 (root4_2, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -20 39 200 -1 minecraft:tuff
fill 20 201 -20 39 210 -1 minecraft:stone
fill 21 201 -19 38 210 -2 minecraft:air
fill 21 209 -19 38 209 -2 minecraft:light[level=15]
fill 30 200 -13 32 200 -12 minecraft:coarse_dirt
fill 20 205 -14 20 208 -9 minecraft:cobblestone
fill 20 206 -17 20 208 -12 minecraft:coal_ore
fill 20 201 -13 20 204 -9 minecraft:deepslate
fill 39 210 -8 39 210 -5 minecraft:deepslate
fill 39 210 -19 39 210 -14 minecraft:coal_ore
fill 39 201 -14 39 202 -13 minecraft:coal_ore
fill 30 201 -20 35 201 -20 minecraft:cobblestone
fill 26 202 -20 26 202 -20 minecraft:deepslate
fill 26 210 -1 31 210 -1 minecraft:coal_ore
fill 31 208 -1 35 210 -1 minecraft:coal_ore
fill 24 210 -1 28 210 -1 minecraft:cobblestone
fill 31 201 -1 34 201 -1 minecraft:spruce_planks
fill 20 210 -20 39 210 -1 minecraft:polished_deepslate
fill 21 210 -19 38 210 -2 minecraft:air
fill 26 201 -5 34 201 -5 minecraft:tuff
fill 25 201 -4 26 201 -2 minecraft:tuff
fill 34 201 -4 35 201 -2 minecraft:tuff
fill 27 201 -4 33 201 -2 minecraft:cobbled_deepslate
fill 27 202 -4 33 202 -2 minecraft:tuff
fill 29 201 -17 29 205 -16 minecraft:deepslate
fill 29 206 -17 29 206 -16 minecraft:tuff
fill 30 201 -17 30 205 -16 minecraft:stone
fill 30 206 -17 30 206 -16 minecraft:tuff
execute positioned 37 201 -11 run function rlk:room/prop/m_rail_z
execute positioned 36 201 -15 run function rlk:room/prop/m_pebble
execute positioned 34 202 -3 run function rlk:room/prop/m_pebble
setblock 38 203 -15 minecraft:wall_torch[facing=west]
setblock 21 203 -5 minecraft:wall_torch[facing=east]
