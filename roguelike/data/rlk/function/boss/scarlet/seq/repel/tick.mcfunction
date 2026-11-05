# CS2 / CS3 repel {at:60|5} (PLAN §3.4): lock, grab, the clash on the hat, the half circle, back to back, the throw, the kick.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 104.
execute if score #sq hr matches 104.. run scoreboard players set #sqdone hr 1
execute if score #sq hr matches ..36 run return run function rlk:boss/scarlet/seq/repel/b/3_36
execute if score #sq hr matches ..102 run return run function rlk:boss/scarlet/seq/repel/b/38_102
