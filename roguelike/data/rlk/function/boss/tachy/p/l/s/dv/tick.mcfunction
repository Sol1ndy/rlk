# L stage dv: one tick (#l_c 1..).
execute if score #l_c tk matches 11..19 at @s run particle minecraft:electric_spark ~ ~ ~ 0.6 0.9 0.6 0.1 3 force @a[tag=player]
execute if score #l_c tk matches 9 run function rlk:boss/tachy/p/l/s/dv/k/9
execute if score #l_c tk matches 10 run function rlk:boss/tachy/p/l/s/dv/k/10
execute if score #l_c tk matches 19 run function rlk:boss/tachy/p/l/s/dv/k/19
execute if score #l_c tk matches 20 run function rlk:boss/tachy/p/l/s/dv/k/20
execute if score #l_c tk matches 30 run function rlk:boss/tachy/p/l/s/dv/k/30
