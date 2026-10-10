# Exact numeric owner, including corpses; never nearest-entity ownership.
tag @e[tag=rlk_fm_this] remove rlk_fm_this
scoreboard players operation #fmId tmp = @s cmId
execute as @e[tag=rlk_fm_rig] if score @s cmId = #fmId tmp run tag @s add rlk_fm_this
