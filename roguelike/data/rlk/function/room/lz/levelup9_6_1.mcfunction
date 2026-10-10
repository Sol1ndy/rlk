# 구역 건설 (levelup9_6, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 40 59 200 59 minecraft:tuff
fill 40 201 40 59 210 59 minecraft:stone
fill 41 201 41 58 210 58 minecraft:air
fill 41 209 41 58 209 58 minecraft:light[level=15]
fill 49 200 43 51 200 45 minecraft:gravel
fill 40 201 48 40 201 52 minecraft:copper_ore
fill 40 205 43 40 207 44 minecraft:tuff
fill 40 205 43 40 208 46 minecraft:deepslate
fill 59 210 53 59 210 56 minecraft:spruce_planks
fill 59 201 40 59 201 43 minecraft:andesite
fill 59 209 43 59 210 44 minecraft:cobblestone
fill 59 203 52 59 203 54 minecraft:spruce_planks
fill 49 207 40 51 207 40 minecraft:andesite
fill 51 204 40 55 205 40 minecraft:deepslate
fill 48 201 40 52 203 40 minecraft:andesite
fill 58 205 40 58 206 40 minecraft:cobblestone
fill 43 204 40 48 207 40 minecraft:cobblestone
fill 48 210 59 52 210 59 minecraft:deepslate
fill 51 210 59 54 210 59 minecraft:copper_ore
fill 52 202 59 56 205 59 minecraft:cobblestone
fill 55 201 50 57 201 50 minecraft:tuff
fill 55 201 51 55 201 54 minecraft:tuff
fill 57 201 51 58 201 51 minecraft:tuff
fill 58 201 52 58 201 52 minecraft:tuff
fill 41 201 55 43 201 55 minecraft:tuff
fill 48 201 55 54 201 55 minecraft:tuff
fill 48 201 56 49 201 56 minecraft:tuff
fill 47 201 57 48 201 58 minecraft:tuff
fill 58 201 58 58 201 58 minecraft:tuff
fill 56 201 51 56 201 54 minecraft:cobbled_deepslate
fill 56 202 51 56 202 54 minecraft:tuff
fill 57 201 52 57 201 52 minecraft:cobbled_deepslate
fill 57 202 52 57 202 52 minecraft:tuff
fill 41 201 54 42 201 54 minecraft:cobbled_deepslate
fill 41 202 54 42 202 54 minecraft:tuff
fill 55 201 55 55 201 55 minecraft:cobbled_deepslate
fill 55 202 55 55 202 55 minecraft:tuff
fill 50 201 56 54 201 56 minecraft:cobbled_deepslate
fill 50 202 56 54 202 56 minecraft:tuff
fill 58 201 56 58 201 57 minecraft:cobbled_deepslate
fill 58 202 56 58 202 57 minecraft:tuff
fill 49 201 57 51 201 58 minecraft:cobbled_deepslate
fill 49 202 57 51 202 58 minecraft:tuff
fill 57 201 57 57 201 58 minecraft:cobbled_deepslate
fill 57 202 57 57 202 58 minecraft:tuff
fill 52 201 58 52 201 58 minecraft:cobbled_deepslate
fill 52 202 58 52 202 58 minecraft:tuff
fill 56 201 58 56 201 58 minecraft:cobbled_deepslate
fill 56 202 58 56 202 58 minecraft:tuff
fill 43 201 54 43 201 54 minecraft:stone
fill 43 202 54 43 202 54 minecraft:tuff
fill 41 201 47 43 202 53 minecraft:cobbled_deepslate
fill 41 203 47 43 203 53 minecraft:tuff
fill 56 201 55 56 202 57 minecraft:cobbled_deepslate
fill 56 203 55 56 203 57 minecraft:tuff
fill 55 201 56 55 202 58 minecraft:cobbled_deepslate
fill 55 203 56 55 203 58 minecraft:tuff
fill 57 201 56 57 202 56 minecraft:cobbled_deepslate
fill 57 203 56 57 203 56 minecraft:tuff
fill 52 201 57 54 202 57 minecraft:cobbled_deepslate
fill 52 203 57 54 203 57 minecraft:tuff
fill 53 201 58 54 202 58 minecraft:cobbled_deepslate
fill 53 203 58 54 203 58 minecraft:tuff
fill 44 201 48 44 202 51 minecraft:deepslate
fill 44 203 48 44 203 51 minecraft:tuff
fill 41 201 46 44 202 46 minecraft:stone
fill 41 203 46 44 203 46 minecraft:tuff
fill 44 201 47 44 202 47 minecraft:stone
fill 44 203 47 44 203 47 minecraft:tuff
fill 44 201 52 44 202 53 minecraft:stone
fill 44 203 52 44 203 53 minecraft:tuff
fill 57 201 54 58 207 55 minecraft:deepslate
fill 57 208 54 58 208 55 minecraft:tuff
fill 57 201 53 58 207 53 minecraft:stone
fill 57 208 53 58 208 53 minecraft:tuff
setblock 41 202 54 minecraft:cobblestone_stairs[facing=north]
setblock 41 201 55 minecraft:cobblestone_stairs[facing=north]
setblock 42 202 54 minecraft:cobblestone_stairs[facing=north]
setblock 42 201 55 minecraft:cobblestone_stairs[facing=north]
setblock 43 202 54 minecraft:cobblestone_stairs[facing=north]
setblock 43 201 55 minecraft:cobblestone_stairs[facing=north]
execute positioned 53 204 58 run function rlk:room/prop/m_crate_a
execute positioned 41 204 52 run function rlk:room/prop/m_torch
execute positioned 52 204 57 run function rlk:room/prop/m_rail_z
execute positioned 48 201 54 run function rlk:room/prop/m_rail_z
setblock 41 206 53 minecraft:wall_torch[facing=east]
setblock 41 203 58 minecraft:wall_torch[facing=east]
