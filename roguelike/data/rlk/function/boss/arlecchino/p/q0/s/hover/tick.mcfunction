# Q0 stage hover: one tick (#q0_c 1..).
execute if score #q0_c kn matches 1..80 run function rlk:mboss/mv/turn {max:10}
execute if score #q0_c kn matches 1..79 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_kn_q0p,distance=..1.5] at @s run return run function rlk:boss/arlecchino/p/q0/s/dive/go
execute if score #q0_c kn matches 4 at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.5 0.8 0.5 0 6 force @a[tag=player]
execute if score #q0_c kn matches 12 at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.5 0.8 0.5 0 6 force @a[tag=player]
execute if score #q0_c kn matches 20 at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.5 0.8 0.5 0 6 force @a[tag=player]
execute if score #q0_c kn matches 28 at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.5 0.8 0.5 0 6 force @a[tag=player]
execute if score #q0_c kn matches 36 at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.5 0.8 0.5 0 6 force @a[tag=player]
execute if score #q0_c kn matches 44 at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.5 0.8 0.5 0 6 force @a[tag=player]
execute if score #q0_c kn matches 52 at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.5 0.8 0.5 0 6 force @a[tag=player]
execute if score #q0_c kn matches 60 at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.5 0.8 0.5 0 6 force @a[tag=player]
execute if score #q0_c kn matches 68 at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.5 0.8 0.5 0 6 force @a[tag=player]
execute if score #q0_c kn matches 76 at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.5 0.8 0.5 0 6 force @a[tag=player]
execute if score #q0_c kn matches 80 run return run function rlk:boss/arlecchino/p/q0/s/hover/k/80
