# Q5B stage main: one tick (#q5b_c 1..).
execute if score #q5b_c kn matches 1..26 run function rlk:mboss/mv/turn {max:10}
execute if score #q5b_c kn matches 50..80 run function rlk:mboss/mv/turn {max:8}
execute if score #q5b_c kn matches 53..79 at @s[tag=!rlk_mb_mv] unless entity @e[tag=rlk_body,limit=1,distance=..3] run function rlk:mboss/mv/step {d:0.15}
execute if score #q5b_c kn matches 6 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.8 0.05 1.8 0 12 force @a[tag=player]
execute if score #q5b_c kn matches 8 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.61 0.05 1.61 0 12 force @a[tag=player]
execute if score #q5b_c kn matches 10 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.43 0.05 1.43 0 12 force @a[tag=player]
execute if score #q5b_c kn matches 12 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.24 0.05 1.24 0 12 force @a[tag=player]
execute if score #q5b_c kn matches 14 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.05 0.05 1.05 0 12 force @a[tag=player]
execute if score #q5b_c kn matches 16 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.86 0.05 0.86 0 12 force @a[tag=player]
execute if score #q5b_c kn matches 18 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.67 0.05 0.67 0 12 force @a[tag=player]
execute if score #q5b_c kn matches 20 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.49 0.05 0.49 0 12 force @a[tag=player]
execute if score #q5b_c kn matches 22 run function rlk:boss/arlecchino/bond/force
execute if score #q5b_c kn matches 26 run function rlk:boss/arlecchino/p/q5b/s/main/k/26
execute if score #q5b_c kn matches 29 run function rlk:boss/arlecchino/p/q5b/f/x_dots
execute if score #q5b_c kn matches 32 run function rlk:boss/arlecchino/p/q5b/f/x_dots
execute if score #q5b_c kn matches 35 run function rlk:boss/arlecchino/p/q5b/f/x_dots
execute if score #q5b_c kn matches 38 run function rlk:boss/arlecchino/p/q5b/s/main/k/38
execute if score #q5b_c kn matches 41 run function rlk:boss/arlecchino/p/q5b/f/x_dots
execute if score #q5b_c kn matches 44 run function rlk:boss/arlecchino/p/q5b/f/x_dots
execute if score #q5b_c kn matches 47 run function rlk:boss/arlecchino/p/q5b/f/x_dots
execute if score #q5b_c kn matches 50 run function rlk:boss/arlecchino/p/q5b/f/x_dots
execute if score #q5b_c kn matches 55 run function rlk:boss/arlecchino/p/q5b/s/main/k/55
execute if score #q5b_c kn matches 56 run function rlk:boss/arlecchino/p/q5b/s/main/k/56
execute if score #q5b_c kn matches 58 run function rlk:boss/arlecchino/p/q5b/s/main/k/58
execute if score #q5b_c kn matches 59 run function rlk:boss/arlecchino/p/q5b/s/main/k/59
execute if score #q5b_c kn matches 61 run function rlk:boss/arlecchino/p/q5b/s/main/k/61
execute if score #q5b_c kn matches 62 run function rlk:boss/arlecchino/p/q5b/s/main/k/62
execute if score #q5b_c kn matches 64 run function rlk:boss/arlecchino/p/q5b/s/main/k/64
execute if score #q5b_c kn matches 65 run function rlk:boss/arlecchino/p/q5b/s/main/k/65
execute if score #q5b_c kn matches 67 run function rlk:boss/arlecchino/p/q5b/s/main/k/67
execute if score #q5b_c kn matches 68 run function rlk:boss/arlecchino/p/q5b/s/main/k/68
execute if score #q5b_c kn matches 70 run function rlk:boss/arlecchino/p/q5b/s/main/k/70
execute if score #q5b_c kn matches 71 run function rlk:boss/arlecchino/p/q5b/s/main/k/71
execute if score #q5b_c kn matches 73 run function rlk:boss/arlecchino/p/q5b/s/main/k/73
execute if score #q5b_c kn matches 74 run function rlk:boss/arlecchino/p/q5b/s/main/k/74
execute if score #q5b_c kn matches 76 run function rlk:boss/arlecchino/p/q5b/s/main/k/76
execute if score #q5b_c kn matches 77 run function rlk:boss/arlecchino/p/q5b/s/main/k/77
execute if score #q5b_c kn matches 78 at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.9 1 0.9 0 12 force @a[tag=player]
execute if score #q5b_c kn matches 79 run function rlk:boss/arlecchino/p/q5b/s/main/k/79
execute if score #q5b_c kn matches 80 run function rlk:boss/arlecchino/p/q5b/s/main/k/80
execute if score #q5b_c kn matches 81 at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.9 1 0.9 0 12 force @a[tag=player]
execute if score #q5b_c kn matches 84 at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.9 1 0.9 0 12 force @a[tag=player]
execute if score #q5b_c kn matches 87 at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.9 1 0.9 0 12 force @a[tag=player]
execute if score #q5b_c kn matches 90 at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.9 1 0.9 0 12 force @a[tag=player]
execute if score #q5b_c kn matches 93 at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.9 1 0.9 0 12 force @a[tag=player]
execute if score #q5b_c kn matches 95 run function rlk:boss/arlecchino/p/q5b/s/main/k/95
execute if score #q5b_c kn matches 96 run function rlk:boss/arlecchino/p/q5b/s/main/k/96
execute if score #q5b_c kn matches 104 run function rlk:boss/arlecchino/rig_stub/look/glow/normal
execute if score #q5b_c kn matches 136 run return run function rlk:boss/arlecchino/p/q5b/s/main/k/136
