# @s = body. The pattern ended (p/end or its max_len): clear the slot and every marker / entity a pattern kept
# (rlk_mb_fg_lock, rlk_mb_fg_kept, rlk_mb_fg_pat: no later run aims at this run's markers), tell the owner.
scoreboard players operation #fgPDone mb = #fgPat mb
scoreboard players set #fgPat mb 0
scoreboard players set #fgPEnd mb 0
scoreboard players set #fgPT mb 0
scoreboard players set #mbNoLeash mb 0
tag @s remove rlk_mb_inv
kill @e[type=minecraft:marker,tag=rlk_mb_fg_lock]
kill @e[type=minecraft:marker,tag=rlk_mb_fg_kept]
kill @e[tag=rlk_mb_fg_pat]
function rlk:mboss/fieldgen/ai/pat_done
scoreboard players set #fgPRel mb 0
