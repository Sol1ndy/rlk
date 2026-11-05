# lead_stand {g:"a8"|"a13"} (PLAN §3.5): the stagger, the hat, the side steps, the refill, the darkness + the brim (the gauntlet g at its end).
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 70.
execute if score #sq hr matches 70.. run scoreboard players set #sqdone hr 1
execute if score #sq hr matches 10 run return run function rlk:boss/scarlet/seq/lead_stand/k/10
execute if score #sq hr matches 18 run return run function rlk:boss/scarlet/seq/lead_stand/k/18
execute if score #sq hr matches 44 run return run function rlk:boss/scarlet/seq/lead_stand/k/44
execute if score #sq hr matches 51 run return run function rlk:boss/scarlet/seq/lead_stand/k/51
