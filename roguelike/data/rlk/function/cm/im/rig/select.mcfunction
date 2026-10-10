# Exact numeric owner, including corpses; never nearest-entity ownership.
tag @e[tag=rlk_im_this] remove rlk_im_this
scoreboard players operation #imId tmp = @s cmId
execute as @e[tag=rlk_im_rig] if score @s cmId = #imId tmp run tag @s add rlk_im_this
