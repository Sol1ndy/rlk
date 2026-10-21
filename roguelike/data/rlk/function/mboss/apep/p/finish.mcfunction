# @s = body. The pattern ended (p/end or its max_len): the slot freed, the kept markers gone, the bookkeeping
# (ai/pat_done: cooldowns, recover, chains, the Q2 count, the opener hand-over), the rest px set of the form.
scoreboard players operation #apPDone mb = #apPid mb
scoreboard players set #apPid mb 0
scoreboard players set #apPEnd mb 0
scoreboard players set #apPT mb 0
scoreboard players set #apYawC mb 0
scoreboard players set #mbNoLeash mb 0
kill @e[type=minecraft:marker,tag=rlk_mb_ap_lock]
kill @e[type=minecraft:marker,tag=rlk_mb_ap_kept]
function rlk:mboss/apep/ai/pat_done
scoreboard players set #apPRel mb 0
scoreboard players set #apHudQ mb 1
