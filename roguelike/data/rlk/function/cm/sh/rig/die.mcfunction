function rlk:cm/sh/rig/select
tag @e[tag=rlk_sh_this] add rlk_sh_dying
tag @e[tag=rlk_sh_this] add rlk_anim_dying
scoreboard players set @s cmAD 0
execute as @e[tag=rlk_sh_this,tag=rlk_sh_part,tag=!rlk_sh_broken] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
function rlk:cm/sh/rig/pose/80
tag @e[tag=rlk_sh_this] remove rlk_sh_this
