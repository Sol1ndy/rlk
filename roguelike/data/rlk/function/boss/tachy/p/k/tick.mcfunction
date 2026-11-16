# K 블링크: one tick; the stage machine (#k_s = stage, #k_c = stage clock).
scoreboard players add #k_c tk 1
execute if score #k_s tk matches 1 run return run function rlk:boss/tachy/p/k/s/out/tick
execute if score #k_s tk matches 2 run return run function rlk:boss/tachy/p/k/s/in/tick
execute if score #k_s tk matches 3 run return run function rlk:boss/tachy/p/k/s/gl/tick
execute if score #k_s tk matches 4 run return run function rlk:boss/tachy/p/k/s/lp/tick
execute if score #k_s tk matches 5 run return run function rlk:boss/tachy/p/k/s/pl/tick
