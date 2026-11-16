# lead_re {g:"a8"|"a13"} (hr_design §3.3; a restart after a pause / the revive): she stands 8 b away, the refill (+ the banner), the hand to the brim; the gauntlet g at its end. Not locked.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 60.
execute if score #sq hr matches 60.. run scoreboard players set #sqdone hr 1
execute if score #sq hr matches 1..9 run return run function rlk:boss/scarlet/seq/lead_re/k/1_9
execute if score #sq hr matches 10 run return run function rlk:boss/scarlet/seq/lead_re/k/10
execute if score #sq hr matches 11..60 run return run function rlk:boss/scarlet/seq/lead_re/k/11_60
