# cmId is the sole ownership key, including the surviving corpse anchor.
tag @e[tag=rlk_sh_this] remove rlk_sh_this
scoreboard players operation #shId tmp = @s cmId
execute as @e[tag=rlk_sh_rig] if score @s cmId = #shId tmp run tag @s add rlk_sh_this
