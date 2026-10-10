# Exact numeric owner, including corpses; never nearest-entity ownership.
tag @e[tag=rlk_ar_this] remove rlk_ar_this
scoreboard players operation #arId tmp = @s cmId
execute as @e[tag=rlk_ar_rig] if score @s cmId = #arId tmp run tag @s add rlk_ar_this
