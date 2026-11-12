# Q5A stage main: one tick (#q5a_c 1..).
execute if score #q5a_c kn matches 1..60 run function rlk:mboss/mv/turn {max:6}
execute if score #q5a_c kn matches 6 at @e[tag=rlk_body,limit=1] run function rlk:boss/arlecchino/fx/p/brand_ring
execute if score #q5a_c kn matches 22 run function rlk:boss/arlecchino/bond/force
execute if score #q5a_c kn matches 60 run function rlk:boss/arlecchino/p/q5a/s/main/k/60
execute if score #q5a_c kn matches 94 run function rlk:boss/arlecchino/p/q5a/s/main/k/94
execute if score #q5a_c kn matches 95 run function rlk:boss/arlecchino/p/q5a/s/main/k/95
execute if score #q5a_c kn matches 100 run function rlk:boss/arlecchino/p/q5a/s/main/k/100
execute if score #q5a_c kn matches 120 run function rlk:boss/arlecchino/p/q5a/s/main/k/120
execute if score #q5a_c kn matches 121 run function rlk:boss/arlecchino/p/q5a/s/main/k/121
execute if score #q5a_c kn matches 130 run function rlk:boss/arlecchino/p/q5a/s/main/k/130
execute if score #q5a_c kn matches 157 run function rlk:boss/arlecchino/p/q5a/s/main/k/157
execute if score #q5a_c kn matches 158 run function rlk:boss/arlecchino/p/q5a/s/main/k/158
execute if score #q5a_c kn matches 166 run function rlk:boss/arlecchino/rig/look/glow/normal
execute if score #q5a_c kn matches 180 run return run function rlk:boss/arlecchino/p/q5a/s/main/k/180
