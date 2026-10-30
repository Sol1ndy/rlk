# @s = brain or corpse anchor; cmId is the sole ownership key
tag @e[tag=rlk_kr_this] remove rlk_kr_this
scoreboard players operation #c2r tmp = @s cmId
execute as @e[tag=rlk_kr_rig] if score @s cmId = #c2r tmp run tag @s add rlk_kr_this
