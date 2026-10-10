# 구역 건설 (normal29_2, 테마 5 사막): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -20 -41 200 -1 minecraft:red_sand
fill -60 201 -20 -41 210 -1 minecraft:smooth_sandstone
fill -59 201 -19 -41 210 -2 minecraft:air
fill -59 209 -19 -41 209 -2 minecraft:light[level=15]
fill -40 200 -20 -21 200 -1 minecraft:red_sand
fill -40 201 -20 -21 210 -1 minecraft:smooth_sandstone
fill -40 201 -19 -22 210 -2 minecraft:air
fill -40 209 -19 -22 209 -2 minecraft:light[level=15]
fill -54 200 -15 -53 200 -14 minecraft:sandstone
fill -54 200 -6 -51 200 -5 minecraft:sand
fill -57 200 -10 -55 200 -7 minecraft:sand
fill -60 209 -12 -60 210 -10 minecraft:terracotta
fill -60 209 -8 -60 210 -7 minecraft:smooth_red_sandstone
fill -60 205 -20 -60 208 -18 minecraft:sandstone
fill -60 201 -20 -60 203 -18 minecraft:cut_sandstone
fill -60 206 -17 -60 207 -16 minecraft:orange_terracotta
fill -47 209 -20 -46 209 -20 minecraft:sandstone
fill -59 206 -20 -55 207 -20 minecraft:terracotta
fill -56 205 -20 -56 205 -20 minecraft:sandstone
fill -46 205 -20 -41 205 -20 minecraft:terracotta
fill -42 210 -20 -42 210 -20 minecraft:sandstone
fill -47 208 -1 -43 208 -1 minecraft:sandstone
fill -55 208 -1 -54 210 -1 minecraft:chiseled_sandstone
fill -47 210 -1 -47 210 -1 minecraft:orange_terracotta
fill -52 203 -1 -47 206 -1 minecraft:cut_sandstone
fill -21 203 -12 -21 204 -9 minecraft:orange_terracotta
fill -21 205 -16 -21 208 -15 minecraft:terracotta
fill -21 202 -7 -21 202 -7 minecraft:cut_sandstone
fill -21 209 -14 -21 210 -11 minecraft:terracotta
fill -21 205 -16 -21 205 -14 minecraft:smooth_red_sandstone
fill -27 204 -20 -22 204 -20 minecraft:orange_terracotta
fill -36 210 -20 -31 210 -20 minecraft:smooth_red_sandstone
fill -40 209 -20 -37 209 -20 minecraft:cut_sandstone
fill -39 207 -1 -38 210 -1 minecraft:red_sandstone
fill -25 203 -1 -22 205 -1 minecraft:orange_terracotta
fill -34 202 -1 -34 205 -1 minecraft:cut_sandstone
fill -39 206 -1 -39 208 -1 minecraft:terracotta
fill -36 210 -1 -31 210 -1 minecraft:cut_sandstone
fill -60 210 -20 -41 210 -1 minecraft:polished_deepslate
fill -59 210 -19 -41 210 -2 minecraft:air
fill -40 210 -20 -21 210 -1 minecraft:polished_deepslate
fill -40 210 -19 -22 210 -2 minecraft:air
fill -24 201 -18 -24 201 -17 minecraft:red_sand
fill -23 201 -17 -23 201 -17 minecraft:red_sand
fill -59 201 -14 -59 201 -4 minecraft:red_sand
fill -33 201 -14 -27 201 -11 minecraft:red_sand
fill -32 201 -10 -31 201 -10 minecraft:red_sand
fill -28 201 -10 -27 201 -9 minecraft:red_sand
fill -31 201 -9 -31 201 -9 minecraft:red_sand
fill -48 201 -10 -46 205 -10 minecraft:smooth_red_sandstone
fill -48 206 -10 -46 206 -10 minecraft:red_sand
fill -48 201 -9 -47 205 -9 minecraft:smooth_red_sandstone
fill -48 206 -9 -47 206 -9 minecraft:red_sand
fill -47 201 -11 -46 205 -11 minecraft:terracotta
fill -47 206 -11 -46 206 -11 minecraft:red_sand
fill -30 201 -10 -29 206 -9 minecraft:smooth_red_sandstone
fill -30 207 -10 -29 207 -9 minecraft:red_sand
fill -42 201 -19 -40 207 -19 minecraft:smooth_red_sandstone
fill -42 208 -19 -40 208 -19 minecraft:red_sand
fill -33 201 -2 -31 207 -2 minecraft:smooth_red_sandstone
fill -33 208 -2 -31 208 -2 minecraft:red_sand
fill -39 201 -19 -39 207 -19 minecraft:terracotta
fill -39 208 -19 -39 208 -19 minecraft:red_sand
fill -30 201 -2 -30 207 -2 minecraft:terracotta
fill -30 208 -2 -30 208 -2 minecraft:red_sand
fill -57 186 -20 -52 199 -15 minecraft:sandstone
fill -57 186 -13 -52 199 -9 minecraft:sandstone
fill -57 186 -7 -52 199 -1 minecraft:sandstone
fill -47 186 -5 -40 199 -1 minecraft:sandstone
fill -56 186 -19 -53 186 -16 minecraft:sandstone
fill -56 187 -19 -53 188 -16 minecraft:sand
fill -56 189 -19 -53 201 -16 minecraft:air
fill -56 186 -12 -53 186 -10 minecraft:sandstone
fill -56 187 -12 -53 188 -10 minecraft:sand
fill -56 189 -12 -53 201 -10 minecraft:air
fill -56 186 -6 -53 186 -2 minecraft:sandstone
fill -56 187 -6 -53 188 -2 minecraft:sand
fill -56 189 -6 -53 201 -2 minecraft:air
fill -46 186 -4 -41 186 -2 minecraft:sandstone
fill -46 187 -4 -41 188 -2 minecraft:sand
fill -46 189 -4 -41 201 -2 minecraft:air
execute positioned -31 201 -6 run function rlk:room/prop/sd_rock_s
execute positioned -30 202 -14 run function rlk:room/prop/sd_rock
execute positioned -47 201 -5 run function rlk:room/prop/sd_obelisk
execute positioned -35 201 -6 run function rlk:room/prop/sd_obelisk
execute positioned -57 201 -13 run function rlk:room/prop/sd_ruin_z
execute positioned -50 201 -14 run function rlk:room/prop/sd_pots
execute positioned -55 201 -7 run function rlk:room/prop/sd_dry
execute positioned -54 201 -4 run function rlk:room/prop/sd_dry
execute positioned -54 201 -18 run function rlk:room/prop/sd_dry
execute positioned -34 201 -9 run function rlk:room/prop/sd_dry
execute positioned -56 201 -13 run function rlk:room/prop/sd_bush
execute positioned -31 202 -13 run function rlk:room/prop/sd_bush
execute positioned -59 202 -8 run function rlk:room/prop/sd_dry
execute positioned -29 201 -2 run function rlk:room/prop/sd_bush
execute positioned -50 201 -7 run function rlk:room/prop/sd_dry
execute positioned -47 201 -13 run function rlk:room/prop/sd_dry
execute positioned -48 201 -14 run function rlk:room/prop/sd_dry
execute positioned -56 201 -6 run function rlk:room/prop/sd_dry
execute positioned -58 201 -4 run function rlk:room/prop/sd_bush
execute positioned -41 201 -11 run function rlk:room/prop/sd_dry
setblock -48 207 -10 minecraft:dead_bush keep
setblock -47 207 -11 minecraft:dead_bush keep
setblock -46 207 -11 minecraft:dead_bush keep
setblock -42 209 -19 minecraft:dead_bush keep
setblock -40 209 -19 minecraft:dead_bush keep
setblock -32 209 -2 minecraft:dead_bush keep
setblock -30 208 -10 minecraft:dead_bush keep
setblock -30 208 -9 minecraft:dead_bush keep
setblock -29 208 -10 minecraft:dead_bush keep
setblock -29 208 -9 minecraft:dead_bush keep
