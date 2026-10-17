# @s = the javelin prop (#pjEv 1 wall / 2 life over): keep it where it stopped until the return (58).
scoreboard players set #pjKeep mb 1
execute at @s run particle minecraft:block{block_state:"minecraft:gold_block"} ^ ^ ^2 0.3 0.3 0.3 0 10 force @a[tag=player]
execute at @s run particle minecraft:end_rod ^ ^ ^2 0.2 0.2 0.2 0.05 4 force @a[tag=player]
execute at @s run playsound minecraft:item.trident.hit_ground hostile @a[tag=player] ~ ~ ~ 0.7 0.9 0.3
