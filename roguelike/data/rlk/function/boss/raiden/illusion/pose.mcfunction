# As a clone husk: its display takes the pose model and the husk's yaw.
scoreboard players operation #rdIlId rd = @s rdObjId
$execute as @e[type=minecraft:item_display,tag=rlk_rd_ilvis] if score @s rdObjId = #rdIlId rd run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/$(model)"
execute rotated as @s as @e[type=minecraft:item_display,tag=rlk_rd_ilvis] if score @s rdObjId = #rdIlId rd positioned as @s run tp @s ~ ~ ~ ~ 0
