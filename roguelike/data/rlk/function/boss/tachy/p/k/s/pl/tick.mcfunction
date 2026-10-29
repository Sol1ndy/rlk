# K stage pl: one tick (#k_c 1..).
execute if score #k_c tk matches 12 positioned as @e[type=minecraft:marker,tag=rlk_tk_klock,limit=1] run function rlk:mboss/mv/glide {t:4}
execute if score #k_c tk matches 15 run function rlk:boss/tachy/p/k/s/pl/k/15
execute if score #k_c tk matches 16 run function rlk:boss/tachy/p/k/s/pl/k/16
execute if score #k_c tk matches 20 run function rlk:boss/tachy/p/k/s/pl/k/20
