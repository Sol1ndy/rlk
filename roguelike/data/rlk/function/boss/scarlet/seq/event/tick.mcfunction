# The event coda (PLAN §7.3.2): item 「검을 건네다」 (the thrown sword) / buff 「월하대작」 (the moonlight orb), the leave, the grant at E56, the black at E110.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 120.
execute if score #sq hr matches 120.. run scoreboard players set #sqdone hr 1
execute if score #sq hr matches ..21 run return run function rlk:boss/scarlet/seq/event/b/4_21
execute if score #sq hr matches ..31 run return run function rlk:boss/scarlet/seq/event/b/22_31
execute if score #sq hr matches ..41 run return run function rlk:boss/scarlet/seq/event/b/32_41
execute if score #sq hr matches ..51 run return run function rlk:boss/scarlet/seq/event/b/42_51
execute if score #sq hr matches ..76 run return run function rlk:boss/scarlet/seq/event/b/52_76
execute if score #sq hr matches ..110 run return run function rlk:boss/scarlet/seq/event/b/80_110
