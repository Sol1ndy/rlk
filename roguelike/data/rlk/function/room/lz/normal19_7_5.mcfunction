# 구역 건설 (normal19_7, 테마 5 사막): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:red_sand
fill -20 201 -60 -1 210 -41 minecraft:smooth_sandstone
fill -19 201 -59 -2 210 -42 minecraft:air
fill -19 209 -59 -2 209 -42 minecraft:light[level=15]
fill -13 200 -55 -12 200 -52 minecraft:cut_sandstone
fill -8 200 -51 -6 200 -48 minecraft:sand
fill -20 208 -60 -20 210 -55 minecraft:cut_sandstone
fill -20 201 -60 -20 204 -58 minecraft:smooth_red_sandstone
fill -20 206 -53 -20 208 -53 minecraft:sandstone
fill -1 208 -50 -1 210 -45 minecraft:smooth_red_sandstone
fill -1 209 -47 -1 210 -43 minecraft:sandstone
fill -1 201 -55 -1 201 -55 minecraft:smooth_red_sandstone
fill -1 206 -42 -1 209 -42 minecraft:cut_sandstone
fill -1 201 -43 -1 204 -41 minecraft:chiseled_sandstone
fill -9 201 -60 -4 203 -60 minecraft:red_sandstone
fill -12 204 -60 -7 206 -60 minecraft:chiseled_sandstone
fill -13 208 -60 -8 210 -60 minecraft:cut_sandstone
fill -13 201 -60 -12 201 -60 minecraft:smooth_red_sandstone
fill -7 203 -41 -7 204 -41 minecraft:red_sandstone
fill -11 209 -41 -8 210 -41 minecraft:cut_sandstone
fill -13 201 -41 -13 203 -41 minecraft:smooth_red_sandstone
fill -16 206 -41 -12 208 -41 minecraft:sandstone
fill -7 207 -41 -2 207 -41 minecraft:smooth_red_sandstone
fill -20 210 -60 -1 210 -41 minecraft:polished_deepslate
fill -19 210 -59 -2 210 -42 minecraft:air
fill -14 201 -45 -6 201 -45 minecraft:red_sand
fill -16 201 -44 -15 201 -42 minecraft:red_sand
fill -6 201 -44 -6 201 -42 minecraft:red_sand
fill -17 201 -43 -17 201 -43 minecraft:red_sand
fill -5 201 -43 -5 201 -43 minecraft:red_sand
fill -14 201 -44 -7 201 -44 minecraft:sandstone
fill -14 202 -44 -7 202 -44 minecraft:red_sand
fill -14 201 -43 -10 201 -42 minecraft:sandstone
fill -14 202 -43 -10 202 -42 minecraft:red_sand
fill -9 201 -42 -7 207 -42 minecraft:smooth_red_sandstone
fill -9 208 -42 -7 208 -42 minecraft:red_sand
fill -9 201 -43 -7 207 -43 minecraft:terracotta
fill -9 208 -43 -7 208 -43 minecraft:red_sand
execute positioned -19 201 -42 run function rlk:room/prop/sd_dry
execute positioned -7 201 -46 run function rlk:room/prop/sd_bush
execute positioned -5 201 -53 run function rlk:room/prop/sd_dry
execute positioned -5 201 -57 run function rlk:room/prop/sd_dry
execute positioned -12 202 -45 run function rlk:room/prop/sd_dry
execute positioned -3 201 -59 run function rlk:room/prop/sd_bush
execute positioned -16 201 -52 run function rlk:room/prop/sd_bush
setblock -9 209 -43 minecraft:dead_bush keep
setblock -8 209 -43 minecraft:dead_bush keep
setblock -7 209 -43 minecraft:dead_bush keep
setblock -7 209 -42 minecraft:dead_bush keep
