# 구역 건설 (normal4_6, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:tuff
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -6 200 -16 -2 200 -14 minecraft:cobblestone
fill -20 202 -18 -20 205 -17 minecraft:andesite
fill -20 208 -6 -20 210 -3 minecraft:cobblestone
fill -20 210 -15 -20 210 -14 minecraft:tuff
fill -1 203 -15 -1 204 -12 minecraft:andesite
fill -1 210 -8 -1 210 -3 minecraft:cobblestone
fill -1 203 -7 -1 203 -3 minecraft:tuff
fill -1 202 -17 -1 203 -16 minecraft:andesite
fill -1 207 -10 -1 207 -8 minecraft:cobblestone
fill -15 201 -20 -15 202 -20 minecraft:spruce_planks
fill -2 202 -20 -1 204 -20 minecraft:iron_ore
fill -11 201 -20 -8 201 -20 minecraft:cobblestone
fill -5 207 -20 -2 208 -20 minecraft:andesite
fill -18 204 -20 -15 206 -20 minecraft:coal_ore
fill -7 210 -1 -3 210 -1 minecraft:coal_ore
fill -13 201 -1 -10 203 -1 minecraft:coal_ore
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -9 201 -5 -7 201 -2 minecraft:tuff
fill -6 201 -4 -2 201 -2 minecraft:tuff
execute positioned -6 202 -4 run function rlk:room/prop/m_fence_x
execute positioned -9 201 -19 run function rlk:room/prop/m_pillar_b
execute positioned -12 201 -16 run function rlk:room/prop/m_pillar_a
execute positioned -12 201 -5 run function rlk:room/prop/m_post
execute positioned -3 201 -8 run function rlk:room/prop/m_rail_z
execute positioned -17 201 -5 run function rlk:room/prop/m_pebble
execute positioned -3 201 -13 run function rlk:room/prop/m_rail_x
execute positioned -16 201 -8 run function rlk:room/prop/m_pebble
setblock -8 204 -2 minecraft:wall_torch[facing=north]
setblock -10 203 -2 minecraft:wall_torch[facing=north]
