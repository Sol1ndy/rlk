# @s = owning husk or corpse anchor. cmId is the sole ownership key.
tag @e[tag=rlk_sw_this] remove rlk_sw_this
scoreboard players operation #swId tmp = @s cmId
execute as @e[tag=rlk_sw_rig] if score @s cmId = #swId tmp run tag @s add rlk_sw_this
