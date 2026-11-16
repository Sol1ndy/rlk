# Q1 stage main: one tick (#q1_c 1..).
execute if score #q1_c kn matches 1..12 at @s[tag=!rlk_mb_mv] unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.2}
execute if score #q1_c kn matches 1..6 run function rlk:mboss/mv/turn {max:12}
execute if score #q1_c kn matches 16..28 at @s[tag=!rlk_mb_mv] unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.3}
execute if score #q1_c kn matches 15..24 run function rlk:mboss/mv/turn {max:14}
execute if score #q1_c kn matches 31..40 run function rlk:mboss/mv/turn {max:14}
execute if score #q1_c kn matches 48..64 at @s[tag=!rlk_mb_mv] unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.3}
execute if score #q1_c kn matches 47..60 run function rlk:mboss/mv/turn {max:14}
execute if score #q1_c kn matches 68..80 at @s[tag=!rlk_mb_mv] unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.3}
execute if score #q1_c kn matches 67..76 run function rlk:mboss/mv/turn {max:14}
execute if score #q1_c kn matches 84..98 at @s[tag=!rlk_mb_mv] unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.3}
execute if score #q1_c kn matches 83..94 run function rlk:mboss/mv/turn {max:14}
execute if score #q1_c kn matches 13 run function rlk:boss/arlecchino/p/q1/s/main/k/13
execute if score #q1_c kn matches 14 run function rlk:boss/arlecchino/p/q1/s/main/k/14
execute if score #q1_c kn matches 29 run function rlk:boss/arlecchino/p/q1/s/main/k/29
execute if score #q1_c kn matches 30 run function rlk:boss/arlecchino/p/q1/s/main/k/30
execute if score #q1_c kn matches 44 at @s unless entity @e[tag=rlk_body,limit=1,distance=..7] run scoreboard players set #q1_k kn 3
execute if score #q1_c kn matches 46 run function rlk:boss/arlecchino/p/q1/s/main/k/46
execute if score #q1_c kn matches 52 run return run function rlk:boss/arlecchino/p/q1/s/main/k/52
execute if score #q1_c kn matches 65 run function rlk:boss/arlecchino/p/q1/s/main/k/65
execute if score #q1_c kn matches 66 run function rlk:boss/arlecchino/p/q1/s/main/k/66
execute if score #q1_c kn matches 80 unless score #q1_k kn matches 3 at @s unless entity @e[tag=rlk_body,limit=1,distance=..7] run scoreboard players set #q1_k kn 5
execute if score #q1_c kn matches 81 run function rlk:boss/arlecchino/p/q1/s/main/k/81
execute if score #q1_c kn matches 82 run function rlk:boss/arlecchino/p/q1/s/main/k/82
execute if score #q1_c kn matches 88 run return run function rlk:boss/arlecchino/p/q1/s/main/k/88
execute if score #q1_c kn matches 100 run function rlk:boss/arlecchino/p/q1/s/main/k/100
execute if score #q1_c kn matches 124 run return run function rlk:boss/arlecchino/p/q1/s/main/k/124
