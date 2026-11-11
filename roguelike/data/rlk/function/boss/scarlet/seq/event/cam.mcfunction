# The event coda (PLAN §7.3.2): item 「검을 건네다」 (the thrown sword) / buff 「월하대작」 (the moonlight orb), the leave, the grant at E56, the black at E110; under the ending's lock until E118.
# The camera lines of this tick (@s = the body; from lock, only while the lock holds).
execute if score #sq hr matches 0..3 run return run function rlk:boss/scarlet/seq/event/cb/0_3
execute if score #sq hr matches 4..25 run return run function rlk:boss/scarlet/seq/event/cb/4_25
execute if score #sq hr matches 26..29 run return run function rlk:boss/scarlet/seq/event/cb/26_29
execute if score #sq hr matches 30..47 run return run function rlk:boss/scarlet/seq/event/cb/30_47
execute if score #sq hr matches 48..51 run return run function rlk:boss/scarlet/seq/event/cb/48_51
execute if score #sq hr matches 52..117 run return run function rlk:boss/scarlet/seq/event/cb/52_117
