# S4 death (@s = body, at it; #mbT 1..100 = the death clip tick): cracks 4, shatter 6, kneel 24,
# dissolve 40.. (motes every 2 t, kit motes every 15 t, shards every 6 t, a descending chime), the last motes 96.
scoreboard players operation #bfM mb = #mbT mb
scoreboard players operation #bfM mb %= #bfK4 mb
execute if score #bfM mb matches 0 if score #mbT mb matches 28..39 run function rlk:mboss/butterfly/seq_h/death/e0_4_28
scoreboard players operation #bfM mb = #mbT mb
scoreboard players operation #bfM mb %= #bfK2 mb
execute if score #bfM mb matches 0 if score #mbT mb matches 40..96 run function rlk:mboss/butterfly/seq_h/death/e1_2_40
execute if score #mbT mb matches 4..61 run return run function rlk:mboss/butterfly/seq_h/death/d/4_61
execute if score #mbT mb matches 67..96 run return run function rlk:mboss/butterfly/seq_h/death/d/67_96
