# The event coda (PLAN §7.3.2): item 「검을 건네다」 (the thrown sword) / buff 「월하대작」 (the moonlight orb), the leave, the grant at E56, the black at E110; under the ending's lock until E118.
# The camera lines of this tick (@s = the body; from lock, only while the lock holds).
execute if score #sq hr matches 0 run return run function rlk:boss/scarlet/seq/event/c/0
execute if score #sq hr matches 1..3 run return run function rlk:boss/scarlet/seq/event/c/1_3
execute if score #sq hr matches 4 run return run function rlk:boss/scarlet/seq/event/c/4
execute if score #sq hr matches 5..117 run return run function rlk:boss/scarlet/seq/event/c/5_117
