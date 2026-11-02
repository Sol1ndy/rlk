# C2 불꽃 도약: one pattern tick (#pt kn = 1..140); events in k/<t>.
execute if score #pt kn matches 1..7 run function rlk:mboss/mv/turn {max:10}
execute if score #pt kn matches 19..43 run function rlk:boss/arlecchino/core/air/drift
execute if score #pt kn matches 19..44 run function rlk:mboss/mv/turn {max:20}
execute if score #pt kn matches 56..88 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt kn matches 55..84 run function rlk:mboss/mv/turn {max:12}
execute if score #pt kn matches 8 run function rlk:boss/arlecchino/p/c2/k/8
execute if score #pt kn matches 18 at @s run playsound minecraft:block.fire.ambient hostile @a[tag=player] ~ ~ ~ 0.8 0.7 0.27
execute if score #pt kn matches 20 at @s run particle minecraft:flame ~ ~ ~ 0.6 0.6 0.6 0.04 8 force @a[tag=player]
execute if score #pt kn matches 24 at @s run particle minecraft:flame ~ ~ ~ 0.6 0.6 0.6 0.04 8 force @a[tag=player]
execute if score #pt kn matches 28 at @s run particle minecraft:flame ~ ~ ~ 0.6 0.6 0.6 0.04 8 force @a[tag=player]
execute if score #pt kn matches 32 at @s run particle minecraft:flame ~ ~ ~ 0.6 0.6 0.6 0.04 8 force @a[tag=player]
execute if score #pt kn matches 36 at @s run particle minecraft:flame ~ ~ ~ 0.6 0.6 0.6 0.04 8 force @a[tag=player]
execute if score #pt kn matches 40 at @s run particle minecraft:flame ~ ~ ~ 0.6 0.6 0.6 0.04 8 force @a[tag=player]
execute if score #pt kn matches 44 run function rlk:boss/arlecchino/p/c2/k/44
execute if score #pt kn matches 48 run function rlk:boss/arlecchino/p/c2/k/48
execute if score #pt kn matches 53 run function rlk:boss/arlecchino/p/c2/k/53
execute if score #pt kn matches 54 run function rlk:boss/arlecchino/p/c2/k/54
execute if score #pt kn matches 78 run function rlk:boss/arlecchino/p/c2/k/78
execute if score #pt kn matches 84 run function rlk:boss/arlecchino/p/c2/k/84
execute if score #pt kn matches 89 run function rlk:boss/arlecchino/p/c2/k/89
execute if score #pt kn matches 90 run function rlk:boss/arlecchino/p/c2/k/90
execute if score #pt kn matches 130 run function rlk:boss/arlecchino/rig_stub/look/wings/off
execute if score #pt kn matches 140 run scoreboard players set #done kn 1
