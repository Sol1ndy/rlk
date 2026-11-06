# @s = body. The pattern ended (p/end or its max_len): clear the slot and tell the owner.
scoreboard players operation #bfPDone mb = #bfPat mb
scoreboard players set #bfPat mb 0
scoreboard players set #bfPEnd mb 0
scoreboard players set #bfPT mb 0
scoreboard players set #mbNoLeash mb 0
tag @s remove rlk_mb_inv
kill @e[type=minecraft:marker,tag=rlk_mb_bf_dest]
kill @e[type=minecraft:marker,tag=rlk_mb_bf_lock]
# every marker a pattern kept (Gen.keep) or summoned for itself (rlk_mb_bf_kept): one run never aims with
# another run's marker (review fix S1 / perf-1)
kill @e[type=minecraft:marker,tag=rlk_mb_bf_kept]
function rlk:mboss/butterfly/ai/pat_done
scoreboard players set #bfPRel mb 0
