# frozen: hold the current pose, still clear the hurt flash
# frozen while vanished: show it (crouched) so a frozen ninja is never invisible
execute if score @s cmAP matches 20 run scoreboard players set #c2p tmp 21
execute if score @s cmAP matches 20 run function rlk:cm/nj/rig/apply
execute if score @s cmAP matches 20 run scoreboard players set @s cmAP 21
execute if score @s cmAH matches 1 as @e[tag=rlk_nj_this,tag=rlk_nj_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_nj_this] remove rlk_nj_this
