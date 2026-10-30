# S1 entrance (@s = body, at it; #mbT = intro clock = entrance clip tick + 1; visuals and sounds only).
# Hover every 4 t, streaks every 8 t, nameplate 57, glow 61, shimmer 69, whiteout 71,
# god rays 75, burst 79, the drop, landing 90.
scoreboard players operation #bfM mb = #mbT mb
scoreboard players operation #bfM mb %= #bfK4 mb
execute if score #bfM mb matches 1 if score #mbT mb matches 5..77 run function rlk:mboss/butterfly/seq_h/entrance/e0_4_4
scoreboard players operation #bfM mb = #mbT mb
scoreboard players operation #bfM mb %= #bfK2 mb
execute if score #bfM mb matches 0 if score #mbT mb matches 62..79 run function rlk:mboss/butterfly/seq_h/entrance/e1_2_61
execute if score #mbT mb matches 1..65 run return run function rlk:mboss/butterfly/seq_h/entrance/d/0_64
execute if score #mbT mb matches 70..103 run return run function rlk:mboss/butterfly/seq_h/entrance/d/69_102
