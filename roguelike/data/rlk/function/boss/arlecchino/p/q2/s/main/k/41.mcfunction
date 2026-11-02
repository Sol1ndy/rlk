# Q2 stage main tick 41
execute at @s run particle minecraft:flame ~ ~ ~ 0.3 0.5 0.3 0.04 10 force @a[tag=player]
execute if score #q2_sl kn matches 1 run function rlk:boss/arlecchino/p/q2/f/h/main_42_0
execute unless score #q2_sl kn matches 1 run function rlk:boss/arlecchino/rig_stub/play/idle2
