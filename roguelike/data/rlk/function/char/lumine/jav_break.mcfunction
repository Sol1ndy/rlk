scoreboard players set #jend tmp 1
execute at @s run particle minecraft:block{block_state:"minecraft:blue_ice"} ~ ~ ~ 0.3 0.3 0.3 0.2 18
execute at @s run particle minecraft:snowflake ~ ~ ~ 0.3 0.3 0.3 0.08 14
execute at @s run playsound minecraft:block.glass.break master @a ~ ~ ~ 0.9 1.3
kill @s
