# Hook resume (@s = body): a pattern's own resume; what the pause left (#grs): the gauntlet's restart (1), the revive
# stance (2), the repel (3), P2 after the judged G1 fail (4), the pending lethal fail (5), CS1's end state (6), the
# repel's end state (7), the lead-in again (8), CS0's end state (9).
execute if score #grs hr matches 1 if score #gk hr matches 1 run function rlk:boss/scarlet/core/lead/re_a8
execute if score #grs hr matches 1 if score #gk hr matches 2 run function rlk:boss/scarlet/core/lead/re_a13
execute if score #grs hr matches 2 run function rlk:boss/scarlet/core/revive/start
execute if score #grs hr matches 3 run function rlk:boss/scarlet/core/repel/start
execute if score #grs hr matches 4 run function rlk:boss/scarlet/core/p2/from_fail
execute if score #grs hr matches 5 run function rlk:boss/scarlet/core/g/fail_now
execute if score #grs hr matches 1 run scoreboard players set #sq hr -1
execute if score #grs hr matches 3 run scoreboard players set #sq hr -1
execute if score #grs hr matches 6 run function rlk:boss/scarlet/core/re/cs1
execute if score #grs hr matches 7 run function rlk:boss/scarlet/core/re/repel
execute if score #grs hr matches 8 run function rlk:boss/scarlet/core/re/lead
execute if score #grs hr matches 9 run function rlk:boss/scarlet/core/intro/reload
scoreboard players set #grs hr 0
