# W2 공중 장풍: one tick; the stage machine (#w2_s = stage, #w2_c = stage clock).
scoreboard players add #w2_c tk 1
execute if score #w2_s tk matches 1 run return run function rlk:boss/tachy/p/w2/s/up/tick
execute if score #w2_s tk matches 2 run return run function rlk:boss/tachy/p/w2/s/air/tick
execute if score #w2_s tk matches 3 run return run function rlk:boss/tachy/p/w2/s/dv/tick
execute if score #w2_s tk matches 4 run return run function rlk:boss/tachy/p/w2/s/ld/tick
