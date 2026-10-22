# S4 death (@s = body, at it; #mbT 1..100 = the death clip tick): cracks 4, shatter 10, kneel 30,
# dissolve 50.. (motes every 2 t, kit motes every 15 t, shards every 6 t, a descending chime), the last motes 96.
scoreboard players operation #bfM mb = #mbT mb
scoreboard players operation #bfM mb %= #bfK4 mb
execute if score #bfM mb matches 2 if score #mbT mb matches 34..49 run function rlk:mboss/butterfly/seq_h/death/e0_4_34
scoreboard players operation #bfM mb = #mbT mb
scoreboard players operation #bfM mb %= #bfK2 mb
execute if score #bfM mb matches 0 if score #mbT mb matches 50..96 run function rlk:mboss/butterfly/seq_h/death/e1_2_50
execute if score #mbT mb matches 4..68 run return run function rlk:mboss/butterfly/seq_h/death/d/4_68
execute if score #mbT mb matches 71..98 run return run function rlk:mboss/butterfly/seq_h/death/d/71_98
