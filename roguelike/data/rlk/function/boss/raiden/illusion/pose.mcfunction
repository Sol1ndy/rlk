# As an illusion husk: swap its display to the pose model.
scoreboard players operation #rdIlId rd = @s rdObjId
$execute as @e[type=minecraft:item_display,tag=rlk_rd_ilvis] if score @s rdObjId = #rdIlId rd run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/$(model)"
