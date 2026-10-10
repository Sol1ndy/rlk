# As an illusion husk at itself: its display follows (teleport_duration smooths it).
scoreboard players operation #rdIlId rd = @s rdObjId
execute as @e[type=minecraft:item_display,tag=rlk_rd_ilvis] if score @s rdObjId = #rdIlId rd run tp @s ~ ~ ~ ~ ~
