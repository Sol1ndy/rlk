scoreboard players operation #t2 itv = #cgRipT itv
scoreboard players operation #t2 itv /= #st4 tmp
scoreboard players operation #t2 itv %= #c3 tmp
execute if score #t2 itv matches 0 run function rlk:items/proc/cg_rip_fx0
execute if score #t2 itv matches 1 run function rlk:items/proc/cg_rip_fx1
execute if score #t2 itv matches 2 run function rlk:items/proc/cg_rip_fx2
