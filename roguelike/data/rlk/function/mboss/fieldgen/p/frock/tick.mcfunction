# frock tick: track the player (3 deg/t), the flying slabs' trails.
function rlk:mboss/mv/turn {max:3}
scoreboard players operation #fgM mb = #fgPT mb
scoreboard players operation #fgM mb %= #fgK2 mb
execute if score #fgM mb matches 0 as @e[type=minecraft:item_display,tag=rlk_mb_fg_p12f] at @s rotated as @s run function rlk:mboss/fieldgen/fx/p/slab_trail
execute if score #fgPT mb matches 8..55 run return run function rlk:mboss/fieldgen/p/frock/d/8_55
execute if score #fgPT mb matches 57..110 run return run function rlk:mboss/fieldgen/p/frock/d/57_110
