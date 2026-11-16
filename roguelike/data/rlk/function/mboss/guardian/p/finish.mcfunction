# @s = body. The pattern ended (p/end or its max_len): clear the slot and tell the owning state.
scoreboard players operation #gdPDone mb = #gdPat mb
scoreboard players set #gdPat mb 0
scoreboard players set #gdPEnd mb 0
scoreboard players set #gdPT mb 0
execute unless score #gdSt mb matches 4 run scoreboard players set #mbNoLeash mb 0
tag @s remove rlk_mb_inv
function rlk:mboss/guardian/ai/pat_done
scoreboard players set #gdPRel mb 0
