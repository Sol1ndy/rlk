# Q5A stage main: one tick (#q5a_c 1..).
execute if score #q5a_c kn matches 1..60 run function rlk:mboss/mv/turn {max:6}
execute if score #q5a_c kn matches 6 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.8 0.05 1.8 0 12 force @a[tag=player]
execute if score #q5a_c kn matches 8 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.61 0.05 1.61 0 12 force @a[tag=player]
execute if score #q5a_c kn matches 10 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.43 0.05 1.43 0 12 force @a[tag=player]
execute if score #q5a_c kn matches 12 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.24 0.05 1.24 0 12 force @a[tag=player]
execute if score #q5a_c kn matches 14 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.05 0.05 1.05 0 12 force @a[tag=player]
execute if score #q5a_c kn matches 16 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.86 0.05 0.86 0 12 force @a[tag=player]
execute if score #q5a_c kn matches 18 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.67 0.05 0.67 0 12 force @a[tag=player]
execute if score #q5a_c kn matches 20 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.49 0.05 0.49 0 12 force @a[tag=player]
execute if score #q5a_c kn matches 22 run function rlk:boss/arlecchino/bond/force
execute if score #q5a_c kn matches 60 run function rlk:boss/arlecchino/p/q5a/s/main/k/60
execute if score #q5a_c kn matches 64 run function rlk:boss/arlecchino/p/q5a/f/dots_60
execute if score #q5a_c kn matches 68 run function rlk:boss/arlecchino/p/q5a/f/dots_60
execute if score #q5a_c kn matches 72 run function rlk:boss/arlecchino/p/q5a/f/dots_60
execute if score #q5a_c kn matches 76 run function rlk:boss/arlecchino/p/q5a/f/dots_60
execute if score #q5a_c kn matches 80 run function rlk:boss/arlecchino/p/q5a/f/dots_60
execute if score #q5a_c kn matches 84 run function rlk:boss/arlecchino/p/q5a/f/dots_60
execute if score #q5a_c kn matches 88 run function rlk:boss/arlecchino/p/q5a/f/dots_60
execute if score #q5a_c kn matches 92 run function rlk:boss/arlecchino/p/q5a/f/dots_60
execute if score #q5a_c kn matches 94 run function rlk:boss/arlecchino/p/q5a/s/main/k/94
execute if score #q5a_c kn matches 95 run function rlk:boss/arlecchino/p/q5a/s/main/k/95
execute if score #q5a_c kn matches 100 run function rlk:boss/arlecchino/p/q5a/s/main/k/100
execute if score #q5a_c kn matches 104 run function rlk:boss/arlecchino/p/q5a/f/dots_100
execute if score #q5a_c kn matches 108 run function rlk:boss/arlecchino/p/q5a/f/dots_100
execute if score #q5a_c kn matches 112 run function rlk:boss/arlecchino/p/q5a/f/dots_100
execute if score #q5a_c kn matches 116 run function rlk:boss/arlecchino/p/q5a/f/dots_100
execute if score #q5a_c kn matches 120 run function rlk:boss/arlecchino/p/q5a/s/main/k/120
execute if score #q5a_c kn matches 121 run function rlk:boss/arlecchino/p/q5a/s/main/k/121
execute if score #q5a_c kn matches 130 run function rlk:boss/arlecchino/p/q5a/s/main/k/130
execute if score #q5a_c kn matches 134 run function rlk:boss/arlecchino/p/q5a/f/dots_130
execute if score #q5a_c kn matches 138 run function rlk:boss/arlecchino/p/q5a/f/dots_130
execute if score #q5a_c kn matches 142 run function rlk:boss/arlecchino/p/q5a/f/dots_130
execute if score #q5a_c kn matches 146 run function rlk:boss/arlecchino/p/q5a/f/dots_130
execute if score #q5a_c kn matches 150 run function rlk:boss/arlecchino/p/q5a/f/dots_130
execute if score #q5a_c kn matches 154 run function rlk:boss/arlecchino/p/q5a/f/dots_130
execute if score #q5a_c kn matches 157 run function rlk:boss/arlecchino/p/q5a/s/main/k/157
execute if score #q5a_c kn matches 158 run function rlk:boss/arlecchino/p/q5a/s/main/k/158
execute if score #q5a_c kn matches 166 run function rlk:boss/arlecchino/rig_stub/look/glow/normal
execute if score #q5a_c kn matches 180 run return run function rlk:boss/arlecchino/p/q5a/s/main/k/180
