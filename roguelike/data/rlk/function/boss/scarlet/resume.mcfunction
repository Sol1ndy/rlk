# Hook resume (@s = body): a pattern's own resume; what a paused gauntlet left (#grs): its restart (1), the revive
# stance (2), the counter cinematic (3), P2 after the judged A8 fail (4), the pending lethal fail (5, core/g/fail_now).
execute if score #grs hr matches 1 if score #gk hr matches 1 run function rlk:boss/scarlet/core/lead/re_a8
execute if score #grs hr matches 1 if score #gk hr matches 2 run function rlk:boss/scarlet/core/lead/re_a13
execute if score #grs hr matches 2 run function rlk:boss/scarlet/core/revive/start
execute if score #grs hr matches 3 run function rlk:boss/scarlet/core/repel/start
execute if score #grs hr matches 4 run function rlk:boss/scarlet/core/p2/from_fail
execute if score #grs hr matches 5 run function rlk:boss/scarlet/core/g/fail_now
execute if score #grs hr matches 1 run scoreboard players set #sq hr -1
execute if score #grs hr matches 3 run scoreboard players set #sq hr -1
scoreboard players set #grs hr 0
