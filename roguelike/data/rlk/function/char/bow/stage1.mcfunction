# 풀차지 도달
scoreboard players set @s bowSt 1
playsound minecraft:block.note_block.pling master @s ~ ~ ~ 0.5 1.6
playsound minecraft:item.firecharge.use master @a ~ ~ ~ 0.4 1.6
execute anchored eyes run particle minecraft:flame ^-0.3 ^-0.25 ^0.9 0.1 0.1 0.1 0.03 8
