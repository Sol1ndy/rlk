# Q0 stage hover: one tick (#q0_c 1..).
execute if score #q0_c kn matches 1..80 run function rlk:mboss/mv/turn {max:10}
execute if score #q0_c kn matches 1..79 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_kn_q0p,distance=..1.5] at @s run return run function rlk:boss/arlecchino/p/q0/s/dive/go
execute if score #q0_c kn matches 80 run return run function rlk:boss/arlecchino/p/q0/s/hover/k/80
