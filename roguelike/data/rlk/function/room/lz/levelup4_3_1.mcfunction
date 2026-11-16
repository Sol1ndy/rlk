# 구역 건설 (levelup4_3, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 20 39 200 39 minecraft:tuff
fill 20 201 20 39 210 39 minecraft:stone
fill 21 201 21 38 210 38 minecraft:air
fill 21 209 21 38 209 38 minecraft:light[level=15]
fill 29 200 34 30 200 35 minecraft:cobblestone
fill 25 200 25 29 200 28 minecraft:gravel
fill 20 202 31 20 205 34 minecraft:cobblestone
fill 20 209 22 20 210 25 minecraft:deepslate
fill 20 202 29 20 203 34 minecraft:cobblestone
fill 20 201 25 20 202 30 minecraft:iron_ore
fill 39 207 27 39 209 29 minecraft:cobblestone
fill 39 206 27 39 207 30 minecraft:cobblestone
fill 39 204 25 39 205 27 minecraft:cobblestone
fill 33 207 20 35 208 20 minecraft:spruce_planks
fill 39 208 20 39 210 20 minecraft:spruce_planks
fill 29 207 20 30 207 20 minecraft:coal_ore
fill 21 201 20 23 202 20 minecraft:copper_ore
fill 22 205 39 23 205 39 minecraft:cobblestone
fill 30 201 39 30 202 39 minecraft:cobblestone
fill 24 206 39 27 209 39 minecraft:tuff
fill 32 209 39 36 210 39 minecraft:andesite
fill 28 209 39 28 210 39 minecraft:cobblestone
fill 20 206 39 23 208 39 minecraft:deepslate
fill 20 210 20 39 210 39 minecraft:polished_deepslate
fill 21 210 21 38 210 38 minecraft:air
fill 33 201 35 33 201 38 minecraft:tuff
fill 32 201 36 32 201 38 minecraft:tuff
fill 34 201 37 34 201 38 minecraft:tuff
fill 35 201 38 38 201 38 minecraft:tuff
execute positioned 25 201 21 run function rlk:room/prop/m_pillar_b
execute positioned 21 201 21 run function rlk:room/prop/m_ore_b
execute positioned 25 201 36 run function rlk:room/prop/m_crate_a
execute positioned 25 201 21 run function rlk:room/prop/m_rail_z
execute positioned 33 202 37 run function rlk:room/prop/m_rail_z
setblock 38 204 25 minecraft:wall_torch[facing=west]
setblock 30 203 38 minecraft:wall_torch[facing=north]
