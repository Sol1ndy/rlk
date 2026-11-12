# 구역 건설 (normal11_6, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 20 -21 200 39 minecraft:tuff
fill -40 201 20 -21 210 39 minecraft:stone
fill -39 201 21 -22 210 38 minecraft:air
fill -39 209 21 -22 209 38 minecraft:light[level=15]
fill -33 200 29 -30 200 30 minecraft:gravel
fill -38 200 26 -37 200 29 minecraft:gravel
fill -40 210 35 -40 210 39 minecraft:andesite
fill -40 205 34 -40 206 39 minecraft:tuff
fill -40 205 36 -40 206 39 minecraft:cobblestone
fill -40 206 30 -40 208 31 minecraft:tuff
fill -21 210 27 -21 210 29 minecraft:spruce_planks
fill -21 203 31 -21 205 35 minecraft:tuff
fill -21 208 22 -21 208 26 minecraft:tuff
fill -24 206 20 -22 206 20 minecraft:tuff
fill -36 206 20 -35 209 20 minecraft:andesite
fill -34 202 20 -32 205 20 minecraft:cobblestone
fill -38 201 39 -35 203 39 minecraft:andesite
fill -37 207 39 -37 209 39 minecraft:copper_ore
fill -37 205 39 -33 205 39 minecraft:coal_ore
fill -40 210 20 -21 210 39 minecraft:polished_deepslate
fill -39 210 21 -22 210 38 minecraft:air
fill -29 201 35 -27 201 38 minecraft:tuff
fill -26 201 36 -22 201 38 minecraft:tuff
fill -34 201 38 -30 206 38 minecraft:stone
fill -34 207 38 -30 207 38 minecraft:tuff
execute positioned -23 201 23 run function rlk:room/prop/m_crate_a
execute positioned -37 201 34 run function rlk:room/prop/m_ore_a
execute positioned -39 201 34 run function rlk:room/prop/m_pebble
execute positioned -35 201 25 run function rlk:room/prop/m_torch
execute positioned -34 201 37 run function rlk:room/prop/m_pebble
setblock -39 203 33 minecraft:wall_torch[facing=east]
setblock -39 203 35 minecraft:wall_torch[facing=east]
