# As a clone husk: remove it and its display where they stand (never moved below the floor).
scoreboard players operation #rdIlId rd = @s rdObjId
execute as @e[type=minecraft:item_display,tag=rlk_rd_ilvis] if score @s rdObjId = #rdIlId rd run kill @s
tag @s remove rlk_rd_illusion
kill @s
