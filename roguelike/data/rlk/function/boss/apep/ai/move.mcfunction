# Phase 1 locomotion (plan 7.3): far band 40 % a crab crawl toward the player; mid band 15 % a side walk.
# Returns 1 when it moved.
execute store result score #apR mb run random value 0..99
execute if score #apBand mb matches 3 if score #apR mb matches ..39 run return run function rlk:boss/apep/ai/move_crawl
execute if score #apBand mb matches 2 if score #apR mb matches ..14 run return run function rlk:boss/apep/ai/move_walk
return fail
