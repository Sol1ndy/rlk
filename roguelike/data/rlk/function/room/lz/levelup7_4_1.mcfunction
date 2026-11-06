# 구역 건설 (levelup7_4, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 40 39 200 59 minecraft:tuff
fill 20 201 40 39 210 59 minecraft:stone
fill 21 201 41 38 210 58 minecraft:air
fill 21 209 41 38 209 58 minecraft:light[level=15]
fill 36 200 50 38 200 53 minecraft:coarse_dirt
fill 25 200 55 27 200 56 minecraft:coarse_dirt
fill 20 205 57 20 205 59 minecraft:tuff
fill 20 203 53 20 206 57 minecraft:cobblestone
fill 39 208 43 39 210 45 minecraft:deepslate
fill 39 208 47 39 210 47 minecraft:andesite
fill 23 209 40 23 209 40 minecraft:cobblestone
fill 30 208 40 32 210 40 minecraft:copper_ore
fill 21 205 40 25 208 40 minecraft:andesite
fill 31 201 59 34 201 59 minecraft:iron_ore
fill 22 210 59 27 210 59 minecraft:coal_ore
fill 20 210 40 39 210 59 minecraft:polished_deepslate
fill 21 210 41 38 210 58 minecraft:air
fill 23 201 42 23 201 49 minecraft:tuff
fill 22 201 43 22 201 49 minecraft:tuff
fill 24 201 46 25 201 49 minecraft:tuff
fill 21 201 47 21 201 49 minecraft:tuff
fill 21 201 44 21 206 46 minecraft:deepslate
fill 21 207 44 21 207 46 minecraft:tuff
fill 21 201 43 21 206 43 minecraft:stone
fill 21 207 43 21 207 43 minecraft:tuff
fill 20 186 51 25 199 57 minecraft:deepslate
fill 21 186 52 24 186 56 minecraft:deepslate
fill 21 187 52 24 188 56 minecraft:lava
fill 21 189 52 24 201 56 minecraft:air
execute positioned 24 202 48 run function rlk:room/prop/m_rubble_a
execute positioned 32 201 56 run function rlk:room/prop/m_post
execute positioned 31 201 47 run function rlk:room/prop/m_rail_x
execute positioned 36 201 50 run function rlk:room/prop/m_rail_x
execute positioned 34 201 57 run function rlk:room/prop/m_rail_x
setblock 27 203 41 minecraft:wall_torch[facing=south]
setblock 22 203 58 minecraft:wall_torch[facing=north]
