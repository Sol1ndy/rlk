# As an illusion husk at its feet: remove it and its display without a death puff.
scoreboard players operation #rdIlId rd = @s rdObjId
execute as @e[type=minecraft:item_display,tag=rlk_rd_ilvis] if score @s rdObjId = #rdIlId rd run kill @s
tag @s remove rlk_rd_illusion
tp @s ~ ~-100 ~
kill @s
