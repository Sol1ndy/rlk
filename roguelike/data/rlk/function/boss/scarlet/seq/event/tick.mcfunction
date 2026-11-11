# The event coda (PLAN §7.3.2): item 「검을 건네다」 (the thrown sword) / buff 「월하대작」 (the moonlight orb), the leave, the grant at E56, the black at E110; under the ending's lock until E118.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 120.
execute if score #sq hr matches 120.. run scoreboard players set #sqdone hr 1
scoreboard players set @a[tag=player] hudHold 2
execute if score #sq hr matches ..117 unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/event/lock
execute if score #sq hr matches 4..32 run return run function rlk:boss/scarlet/seq/event/kb/4_32
execute if score #sq hr matches 33..38 run return run function rlk:boss/scarlet/seq/event/kb/33_38
execute if score #sq hr matches 39..44 run return run function rlk:boss/scarlet/seq/event/kb/39_44
execute if score #sq hr matches 45..51 run return run function rlk:boss/scarlet/seq/event/kb/45_51
execute if score #sq hr matches 52..60 run return run function rlk:boss/scarlet/seq/event/kb/52_60
execute if score #sq hr matches 64..84 run return run function rlk:boss/scarlet/seq/event/kb/64_84
execute if score #sq hr matches 88..108 run return run function rlk:boss/scarlet/seq/event/kb/88_108
execute if score #sq hr matches 110..118 run return run function rlk:boss/scarlet/seq/event/kb/110_118
