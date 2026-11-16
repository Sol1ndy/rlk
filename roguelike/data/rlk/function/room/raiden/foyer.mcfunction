# @s = zone 1 marker at map generation: the entrance pier with its torii (the native door fills the torii),
# invisible barriers around it, its light; then the Plane of Euthymia backdrop is built in slices.
fill -6 201 24 5 230 39 minecraft:air strict
fill -6 200 24 -6 200 39 minecraft:light_blue_concrete_powder strict
fill -5 200 24 -5 200 38 minecraft:polished_deepslate strict
fill -4 200 24 -3 200 37 minecraft:dark_prismarine strict
fill -2 200 24 1 200 37 minecraft:deepslate_tiles strict
fill 2 200 24 3 200 37 minecraft:dark_prismarine strict
fill 4 200 24 4 200 38 minecraft:polished_deepslate strict
fill 5 200 24 5 200 25 minecraft:cyan_concrete_powder strict
fill 5 200 26 5 200 30 minecraft:light_blue_concrete_powder strict
setblock 5 200 31 minecraft:cyan_concrete_powder strict
fill 5 200 32 5 200 37 minecraft:light_blue_concrete_powder strict
fill -4 200 38 3 200 38 minecraft:polished_deepslate strict
setblock 5 200 38 minecraft:light_blue_wool strict
fill -5 200 39 -4 200 39 minecraft:light_blue_concrete_powder strict
setblock -3 200 39 minecraft:light_blue_wool strict
fill -2 200 39 1 200 39 minecraft:light_blue_concrete_powder strict
setblock 2 200 39 minecraft:light_blue_wool strict
fill 3 200 39 5 200 39 minecraft:light_blue_concrete_powder strict
fill -6 201 24 -4 206 24 minecraft:barrier strict
fill -3 201 24 -3 209 24 minecraft:red_concrete strict
fill 2 201 24 2 209 24 minecraft:red_concrete strict
fill 3 201 24 5 206 24 minecraft:barrier strict
fill -6 201 25 -6 210 39 minecraft:barrier strict
setblock -5 201 25 minecraft:chiseled_stone_bricks strict
setblock 4 201 25 minecraft:chiseled_stone_bricks strict
fill 5 201 25 5 210 39 minecraft:barrier strict
fill -5 201 39 4 210 39 minecraft:barrier strict
setblock -5 202 25 minecraft:soul_lantern strict
setblock 4 202 25 minecraft:soul_lantern strict
fill -5 204 25 4 204 38 minecraft:light[level=15] strict
fill -6 207 24 -5 208 24 minecraft:barrier strict
setblock -4 207 24 minecraft:red_concrete strict
setblock 3 207 24 minecraft:red_concrete strict
fill 4 207 24 5 208 24 minecraft:barrier strict
setblock -4 208 24 minecraft:barrier strict
fill -1 208 24 0 208 24 minecraft:black_concrete strict
setblock 3 208 24 minecraft:barrier strict
setblock -6 209 24 minecraft:barrier strict
fill -5 209 24 -4 209 24 minecraft:red_concrete strict
fill -2 209 24 1 209 24 minecraft:red_concrete strict
fill 3 209 24 4 209 24 minecraft:red_concrete strict
setblock 5 209 24 minecraft:barrier strict
fill -6 210 24 5 210 24 minecraft:black_concrete strict
tag @s add rlk_rd_bgzone
function rlk:room/raiden/bg/start
