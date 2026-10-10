tag @e[tag=rlk_cn_this] remove rlk_cn_this
scoreboard players operation #cnId tmp = @s cmId
execute as @e[tag=rlk_cn_rig] if score @s cmId = #cnId tmp run tag @s add rlk_cn_this
