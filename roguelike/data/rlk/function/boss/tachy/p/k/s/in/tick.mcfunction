# K stage in: one tick (#k_c 1..).
execute if score #k_c tk matches 1..200 run function rlk:mboss/mv/turn {max:8}
execute if score #k_c tk matches 10 run function rlk:boss/tachy/rig/play/k_hold
execute if score #k_c tk >= #k_h tk run return run function rlk:boss/tachy/p/k/s/gl/go
