scoreboard players set @s cmAH 6
function rlk:cm/sh/rig/select
execute as @e[tag=rlk_sh_this,tag=rlk_sh_part,tag=!rlk_sh_broken] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16737903]}
tag @e[tag=rlk_sh_this] remove rlk_sh_this
