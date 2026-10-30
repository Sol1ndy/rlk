# 구역 건설 (normal21_6, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:tuff
fill -20 201 -60 -1 210 -41 minecraft:stone
fill -19 201 -59 -2 210 -42 minecraft:air
fill -19 209 -59 -2 209 -42 minecraft:light[level=15]
fill -10 200 -55 -8 200 -53 minecraft:cobblestone
fill -9 200 -51 -7 200 -50 minecraft:gravel
fill -20 208 -52 -20 210 -50 minecraft:deepslate
fill -1 209 -52 -1 210 -48 minecraft:deepslate
fill -1 206 -42 -1 209 -41 minecraft:cobblestone
fill -18 205 -60 -14 206 -60 minecraft:copper_ore
fill -6 203 -60 -5 205 -60 minecraft:tuff
fill -4 202 -60 -3 205 -60 minecraft:cobblestone
fill -16 205 -41 -13 205 -41 minecraft:cobblestone
fill -10 207 -41 -9 207 -41 minecraft:copper_ore
fill -16 202 -41 -15 202 -41 minecraft:iron_ore
fill -10 201 -41 -8 204 -41 minecraft:deepslate
fill -20 210 -60 -1 210 -41 minecraft:polished_deepslate
fill -19 210 -59 -2 210 -42 minecraft:air
fill -19 201 -44 -17 201 -44 minecraft:tuff
fill -17 201 -43 -17 201 -42 minecraft:tuff
fill -19 201 -43 -18 201 -42 minecraft:cobbled_deepslate
fill -19 202 -43 -18 202 -42 minecraft:tuff
fill -12 201 -59 -8 205 -59 minecraft:deepslate
fill -12 206 -59 -8 206 -59 minecraft:tuff
fill -13 201 -59 -13 205 -59 minecraft:stone
fill -13 206 -59 -13 206 -59 minecraft:tuff
execute positioned -2 201 -54 run function rlk:room/prop/m_arch_z6
execute positioned -13 201 -55 run function rlk:room/prop/m_fence_x
execute positioned -2 201 -46 run function rlk:room/prop/m_fence_z
execute positioned -17 201 -58 run function rlk:room/prop/m_pebble
execute positioned -10 201 -50 run function rlk:room/prop/m_rail_z
execute positioned -12 201 -52 run function rlk:room/prop/m_rail_z
setblock -2 203 -51 minecraft:wall_torch[facing=west]
setblock -2 203 -53 minecraft:wall_torch[facing=west]
