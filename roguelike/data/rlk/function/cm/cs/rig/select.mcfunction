# @s = brain or corpse anchor; cmId is the sole ownership key
tag @e[tag=rlk_cs_this] remove rlk_cs_this
scoreboard players operation #c2r tmp = @s cmId
execute as @e[tag=rlk_cs_rig] if score @s cmId = #c2r tmp run tag @s add rlk_cs_this
