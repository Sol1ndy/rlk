# C1 불꽃 도약: one pattern tick (#pt kn = 1..80); events in k/<t>.
execute if score #pt kn matches 1..7 run function rlk:mboss/mv/turn {max:10}
execute if score #pt kn matches 19..43 run function rlk:boss/arlecchino/core/air/drift
execute if score #pt kn matches 19..44 run function rlk:mboss/mv/turn {max:20}
execute if score #pt kn matches 8 run function rlk:boss/arlecchino/p/c1/k/8
execute if score #pt kn matches 18 at @s run function rlk:boss/arlecchino/fx/snd/apex
execute if score #pt kn matches 20 at @s run particle minecraft:flame ~ ~ ~ 0.6 0.6 0.6 0.04 8 force @a[tag=player]
execute if score #pt kn matches 24 at @s run particle minecraft:flame ~ ~ ~ 0.6 0.6 0.6 0.04 8 force @a[tag=player]
execute if score #pt kn matches 28 at @s run particle minecraft:flame ~ ~ ~ 0.6 0.6 0.6 0.04 8 force @a[tag=player]
execute if score #pt kn matches 32 at @s run particle minecraft:flame ~ ~ ~ 0.6 0.6 0.6 0.04 8 force @a[tag=player]
execute if score #pt kn matches 36 at @s run particle minecraft:flame ~ ~ ~ 0.6 0.6 0.6 0.04 8 force @a[tag=player]
execute if score #pt kn matches 40 at @s run particle minecraft:flame ~ ~ ~ 0.6 0.6 0.6 0.04 8 force @a[tag=player]
execute if score #pt kn matches 44 run function rlk:boss/arlecchino/p/c1/k/44
execute if score #pt kn matches 48 run function rlk:boss/arlecchino/p/c1/k/48
execute if score #pt kn matches 53 run function rlk:boss/arlecchino/p/c1/k/53
execute if score #pt kn matches 54 run function rlk:boss/arlecchino/p/c1/k/54
execute if score #pt kn matches 80 run scoreboard players set #done kn 1
