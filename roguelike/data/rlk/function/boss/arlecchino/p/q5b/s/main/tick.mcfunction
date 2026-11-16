# Q5B stage main: one tick (#q5b_c 1..).
execute if score #q5b_c kn matches 1..26 run function rlk:mboss/mv/turn {max:10}
execute if score #q5b_c kn matches 50..80 run function rlk:mboss/mv/turn {max:8}
execute if score #q5b_c kn matches 53..79 at @s[tag=!rlk_mb_mv] unless entity @e[tag=rlk_body,limit=1,distance=..3] run function rlk:mboss/mv/step {d:0.15}
execute if score #q5b_c kn matches 6 at @e[tag=rlk_body,limit=1] run function rlk:boss/arlecchino/fx/p/brand_ring
execute if score #q5b_c kn matches 22 run function rlk:boss/arlecchino/bond/force
execute if score #q5b_c kn matches 26 run function rlk:boss/arlecchino/p/q5b/s/main/k/26
execute if score #q5b_c kn matches 38 at @s run function rlk:boss/arlecchino/fx/snd/x_carve
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
execute if score #q5b_c kn matches 79 run function rlk:boss/arlecchino/p/q5b/s/main/k/79
execute if score #q5b_c kn matches 80 run function rlk:boss/arlecchino/p/q5b/s/main/k/80
execute if score #q5b_c kn matches 95 run function rlk:boss/arlecchino/p/q5b/s/main/k/95
execute if score #q5b_c kn matches 96 run function rlk:boss/arlecchino/p/q5b/s/main/k/96
execute if score #q5b_c kn matches 104 run function rlk:boss/arlecchino/rig/look/glow/normal
execute if score #q5b_c kn matches 136 run return run function rlk:boss/arlecchino/p/q5b/s/main/k/136
