# @s = brain or corpse anchor; cmId is the sole ownership key
tag @e[tag=rlk_pc_this] remove rlk_pc_this
scoreboard players operation #c2r tmp = @s cmId
execute as @e[tag=rlk_pc_rig] if score @s cmId = #c2r tmp run tag @s add rlk_pc_this
