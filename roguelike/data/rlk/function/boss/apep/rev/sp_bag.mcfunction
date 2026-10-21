# A special from the bag {수호, 둥지, 양육, 포식성} (the stub draws at random).
execute store result score #apR mb run random value 0..3
execute if score #apR mb matches 0 run return run function rlk:boss/apep/rev/sp_guard
execute if score #apR mb matches 1 run return run function rlk:boss/apep/rev/sp_nest
execute if score #apR mb matches 2 run return run function rlk:boss/apep/rev/sp_nurt
execute if score #apR mb matches 3 run return run function rlk:boss/apep/rev/sp_pred
