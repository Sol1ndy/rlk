# The event coda (PLAN §7.3.2): item 「검을 건네다」 (the thrown sword) / buff 「월하대작」 (the moonlight orb), the leave, the grant at E56, the black at E110; under the ending's lock until E118.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 120.
execute if score #sq hr matches 120.. run scoreboard players set #sqdone hr 1
scoreboard players set @a[tag=player] hudHold 2
execute if score #sq hr matches ..117 unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/event/lock
execute if score #sq hr matches 4..15 run return run function rlk:boss/scarlet/seq/event/kb/4_15
execute if score #sq hr matches 16..30 run return run function rlk:boss/scarlet/seq/event/kb/16_30
execute if score #sq hr matches 31..37 run return run function rlk:boss/scarlet/seq/event/kb/31_37
execute if score #sq hr matches 38..44 run return run function rlk:boss/scarlet/seq/event/kb/38_44
execute if score #sq hr matches 45..52 run return run function rlk:boss/scarlet/seq/event/kb/45_52
execute if score #sq hr matches 53..68 run return run function rlk:boss/scarlet/seq/event/kb/53_68
execute if score #sq hr matches 72..96 run return run function rlk:boss/scarlet/seq/event/kb/72_96
execute if score #sq hr matches 100..118 run return run function rlk:boss/scarlet/seq/event/kb/100_118
