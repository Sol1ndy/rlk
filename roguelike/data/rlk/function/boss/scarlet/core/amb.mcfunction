# The arena ambience (@s = body; PLAN §6.3 / §6.4): ambient_p1 every 10 t at each player in P1, ambient_p2
# every 6 t in P2, the down window and the gauntlets; none in a sequence (it stages its own effects).
scoreboard players operation #t hr = #clk hr
execute if score #ph hr matches 1 run return run function rlk:boss/scarlet/core/amb1
execute if score #ph hr matches 4..9 unless score #ph hr matches 5 unless score #ph hr matches 8 run function rlk:boss/scarlet/core/amb2
