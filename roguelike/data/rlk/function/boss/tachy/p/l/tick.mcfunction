# L 착지 공격: one tick; the stage machine (#l_s = stage, #l_c = stage clock).
scoreboard players add #l_c tk 1
execute if score #l_s tk matches 1 run return run function rlk:boss/tachy/p/l/s/up/tick
execute if score #l_s tk matches 2 run return run function rlk:boss/tachy/p/l/s/hv/tick
execute if score #l_s tk matches 3 run return run function rlk:boss/tachy/p/l/s/dv/tick
