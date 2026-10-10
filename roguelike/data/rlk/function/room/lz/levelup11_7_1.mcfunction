# 구역 건설 (levelup11_7, 테마 1): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 40 -41 200 59 minecraft:tuff
fill -60 201 40 -41 210 59 minecraft:stone
fill -59 201 41 -42 210 58 minecraft:air
fill -59 209 41 -42 209 58 minecraft:light[level=15]
fill -60 210 40 -60 210 43 minecraft:deepslate
fill -60 207 53 -60 208 53 minecraft:cobblestone
fill -60 207 54 -60 208 56 minecraft:andesite
fill -60 203 55 -60 205 55 minecraft:coal_ore
fill -41 207 49 -41 207 54 minecraft:cobblestone
fill -41 206 47 -41 209 48 minecraft:copper_ore
fill -41 203 57 -41 203 59 minecraft:cobblestone
fill -41 208 55 -41 209 57 minecraft:spruce_planks
fill -41 209 54 -41 210 57 minecraft:tuff
fill -41 210 52 -41 210 54 minecraft:tuff
fill -44 205 40 -42 205 40 minecraft:deepslate
fill -44 210 40 -42 210 40 minecraft:spruce_planks
fill -51 202 40 -48 204 40 minecraft:tuff
fill -52 207 59 -47 210 59 minecraft:coal_ore
fill -46 207 59 -46 209 59 minecraft:tuff
fill -46 204 59 -45 205 59 minecraft:iron_ore
fill -60 208 59 -57 210 59 minecraft:andesite
fill -54 206 59 -54 209 59 minecraft:copper_ore
fill -50 209 59 -45 210 59 minecraft:deepslate
fill -44 201 44 -42 201 44 minecraft:tuff
fill -59 201 47 -56 201 57 minecraft:tuff
fill -55 201 55 -49 201 55 minecraft:tuff
fill -55 201 56 -55 201 56 minecraft:tuff
fill -49 201 56 -49 201 56 minecraft:tuff
fill -48 201 57 -48 201 58 minecraft:tuff
fill -56 201 58 -56 201 58 minecraft:tuff
fill -43 201 45 -42 201 45 minecraft:cobbled_deepslate
fill -43 202 45 -42 202 45 minecraft:tuff
fill -54 201 56 -50 201 56 minecraft:cobbled_deepslate
fill -54 202 56 -50 202 56 minecraft:tuff
fill -55 201 57 -55 201 58 minecraft:cobbled_deepslate
fill -55 202 57 -55 202 58 minecraft:tuff
fill -49 201 57 -49 201 58 minecraft:cobbled_deepslate
fill -49 202 57 -49 202 58 minecraft:tuff
fill -44 201 45 -44 201 45 minecraft:deepslate
fill -44 202 45 -44 202 45 minecraft:tuff
fill -44 201 46 -42 202 52 minecraft:cobbled_deepslate
fill -44 203 46 -42 203 52 minecraft:tuff
fill -54 201 57 -50 202 58 minecraft:cobbled_deepslate
fill -54 203 57 -50 203 58 minecraft:tuff
fill -45 201 52 -45 202 53 minecraft:deepslate
fill -45 203 52 -45 203 53 minecraft:tuff
fill -44 201 53 -43 202 53 minecraft:deepslate
fill -44 203 53 -43 203 53 minecraft:tuff
fill -45 201 46 -45 202 51 minecraft:stone
fill -45 203 46 -45 203 51 minecraft:tuff
fill -42 201 53 -42 202 53 minecraft:stone
fill -42 203 53 -42 203 53 minecraft:tuff
fill -59 201 44 -59 205 45 minecraft:deepslate
fill -59 206 44 -59 206 45 minecraft:tuff
fill -59 201 41 -59 205 43 minecraft:stone
fill -59 206 41 -59 206 43 minecraft:tuff
setblock -44 201 44 minecraft:cobblestone_stairs[facing=south]
setblock -44 202 45 minecraft:cobblestone_stairs[facing=south]
setblock -43 201 44 minecraft:cobblestone_stairs[facing=south]
setblock -43 202 45 minecraft:cobblestone_stairs[facing=south]
setblock -42 201 44 minecraft:cobblestone_stairs[facing=south]
setblock -42 202 45 minecraft:cobblestone_stairs[facing=south]
execute positioned -53 201 51 run function rlk:room/prop/m_rail_x
execute positioned -57 202 55 run function rlk:room/prop/m_pebble
execute positioned -48 202 58 run function rlk:room/prop/m_rail_z
setblock -42 203 41 minecraft:wall_torch[facing=south]
setblock -42 203 57 minecraft:wall_torch[facing=west]
