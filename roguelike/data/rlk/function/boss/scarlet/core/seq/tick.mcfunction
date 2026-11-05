# A sequence tick of the fight state (@s = body): #sq + 1, seq/<name>/tick, its signal (#sq_sig, read right after the
# tick), its end (#sqdone).
scoreboard players add #sq hr 1
execute if score #sqn hr matches 2 run function rlk:boss/scarlet/seq/cs1/tick
execute if score #sqn hr matches 3 run function rlk:boss/scarlet/seq/sq1/tick
execute if score #sqn hr matches 4 run function rlk:boss/scarlet/seq/repel/tick
execute if score #sqn hr matches 5 run function rlk:boss/scarlet/seq/lead_down/tick
execute if score #sqn hr matches 6 run function rlk:boss/scarlet/seq/lead_stand/tick
execute if score #sq_sig hr matches 1.. run function rlk:boss/scarlet/core/sig
execute unless score #mbSt mb matches 1 run return 0
execute if score #sqdone hr matches 1 run function rlk:boss/scarlet/core/seq/end
