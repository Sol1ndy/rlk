# @s = brain or corpse anchor; cmId is the sole ownership key
tag @e[tag=rlk_ci_this] remove rlk_ci_this
scoreboard players operation #c2r tmp = @s cmId
execute as @e[tag=rlk_ci_rig] if score @s cmId = #c2r tmp run tag @s add rlk_ci_this
