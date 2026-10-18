# waves tick: track the player (3 deg/t), the decals again after a pause, the fronts grow (before hz/all).
function rlk:mboss/mv/turn {max:3}
execute if score #fq21P mb matches 1 run function rlk:mboss/fieldgen/p/waves/redraw
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p21f] run function rlk:mboss/fieldgen/p/waves/grow
execute if score #fgPT mb matches 8..113 run return run function rlk:mboss/fieldgen/p/waves/d/8_113
execute if score #fgPT mb matches 116..224 run return run function rlk:mboss/fieldgen/p/waves/d/116_224
