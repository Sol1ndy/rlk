# 구역 건설 (levelup2_5, 테마 5 사막): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -40 -41 200 -21 minecraft:red_sand
fill -60 201 -40 -41 210 -21 minecraft:smooth_sandstone
fill -59 201 -39 -42 210 -22 minecraft:air
fill -59 209 -39 -42 209 -22 minecraft:light[level=15]
fill -45 200 -32 -43 200 -31 minecraft:smooth_sandstone
fill -46 200 -30 -42 200 -29 minecraft:sand
fill -60 201 -34 -60 201 -31 minecraft:red_sandstone
fill -60 210 -37 -60 210 -37 minecraft:chiseled_sandstone
fill -60 203 -37 -60 204 -37 minecraft:sandstone
fill -60 209 -28 -60 210 -23 minecraft:cut_sandstone
fill -41 201 -30 -41 203 -25 minecraft:orange_terracotta
fill -41 206 -39 -41 206 -34 minecraft:terracotta
fill -41 208 -23 -41 208 -23 minecraft:orange_terracotta
fill -55 201 -40 -52 201 -40 minecraft:terracotta
fill -59 206 -21 -56 207 -21 minecraft:red_sandstone
fill -52 207 -21 -48 208 -21 minecraft:smooth_red_sandstone
fill -54 206 -21 -54 208 -21 minecraft:orange_terracotta
fill -60 210 -40 -41 210 -21 minecraft:polished_deepslate
fill -59 210 -39 -42 210 -22 minecraft:air
fill -59 201 -35 -56 201 -35 minecraft:red_sand
fill -56 201 -34 -55 201 -34 minecraft:red_sand
fill -55 201 -33 -55 201 -27 minecraft:red_sand
fill -56 201 -27 -56 201 -27 minecraft:red_sand
fill -57 201 -26 -57 201 -23 minecraft:red_sand
fill -59 201 -23 -58 201 -23 minecraft:red_sand
fill -59 201 -34 -57 201 -33 minecraft:sandstone
fill -59 202 -34 -57 202 -33 minecraft:red_sand
fill -56 201 -33 -56 201 -28 minecraft:sandstone
fill -56 202 -33 -56 202 -28 minecraft:red_sand
fill -57 201 -27 -57 201 -27 minecraft:sandstone
fill -57 202 -27 -57 202 -27 minecraft:red_sand
fill -58 201 -26 -58 201 -24 minecraft:sandstone
fill -58 202 -26 -58 202 -24 minecraft:red_sand
fill -59 201 -25 -59 201 -24 minecraft:sandstone
fill -59 202 -25 -59 202 -24 minecraft:red_sand
fill -59 201 -32 -57 202 -28 minecraft:sandstone
fill -59 203 -32 -57 203 -28 minecraft:red_sand
fill -59 201 -27 -58 202 -27 minecraft:sandstone
fill -59 203 -27 -58 203 -27 minecraft:red_sand
fill -59 201 -26 -59 202 -26 minecraft:sandstone
fill -59 203 -26 -59 203 -26 minecraft:red_sand
fill -54 201 -39 -52 205 -38 minecraft:smooth_red_sandstone
fill -54 206 -39 -52 206 -38 minecraft:red_sand
fill -51 201 -39 -50 205 -38 minecraft:terracotta
fill -51 206 -39 -50 206 -38 minecraft:red_sand
fill -56 201 -36 -55 207 -36 minecraft:smooth_red_sandstone
fill -56 208 -36 -55 208 -36 minecraft:red_sand
fill -56 201 -37 -55 207 -37 minecraft:terracotta
fill -56 208 -37 -55 208 -37 minecraft:red_sand
execute positioned -51 201 -35 run function rlk:room/prop/sd_rock_s
execute positioned -56 203 -33 run function rlk:room/prop/sd_obelisk
execute positioned -48 201 -36 run function rlk:room/prop/sd_bush
execute positioned -57 201 -38 run function rlk:room/prop/sd_dry
execute positioned -59 204 -26 run function rlk:room/prop/sd_bush
execute positioned -58 204 -31 run function rlk:room/prop/sd_bush
execute positioned -47 201 -31 run function rlk:room/prop/sd_bush
execute positioned -48 201 -31 run function rlk:room/prop/sd_dry
execute positioned -45 201 -39 run function rlk:room/prop/sd_bush
setblock -56 209 -36 minecraft:dead_bush keep
setblock -55 209 -37 minecraft:dead_bush keep
setblock -53 207 -39 minecraft:dead_bush keep
setblock -53 207 -38 minecraft:dead_bush keep
setblock -52 207 -39 minecraft:dead_bush keep
setblock -52 207 -38 minecraft:dead_bush keep
setblock -50 207 -39 minecraft:dead_bush keep
