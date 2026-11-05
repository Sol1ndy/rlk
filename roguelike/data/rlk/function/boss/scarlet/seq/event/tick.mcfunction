# The event coda (PLAN §7.3.2): item 「검을 건네다」 (the thrown sword) / buff 「월하대작」 (the moonlight orb), the leave, the grant at E56, the black at E110.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 120.
execute if score #sq hr matches 120.. run scoreboard players set #sqdone hr 1
execute if score #sq hr matches ..39 run return run function rlk:boss/scarlet/seq/event/b/30_39
execute if score #sq hr matches ..49 run return run function rlk:boss/scarlet/seq/event/b/40_49
execute if score #sq hr matches ..56 run return run function rlk:boss/scarlet/seq/event/b/50_56
