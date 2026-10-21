# @s = body. The pattern ended (p/end or its max_len): clear the slot and every marker it kept (no later run aims
# at them), then the bookkeeping (ai/pat_done: services advance the transition).
scoreboard players operation #azPDone mb = #azPat mb
scoreboard players set #azPat mb 0
scoreboard players set #azPEnd mb 0
scoreboard players set #azPT mb 0
scoreboard players set #mbNoLeash mb 0
kill @e[type=minecraft:marker,tag=rlk_mb_az_lock]
kill @e[type=minecraft:marker,tag=rlk_mb_az_kept]
function rlk:mboss/azhdaha/ai/pat_done
scoreboard players set #azPRel mb 0
scoreboard players set #azHudQ mb 1
