# Called once as boss, before its rig; position is refreshed after relocation.
execute unless score @s rdBlink matches 1.. run return 0
execute if score @s rdBlink matches 4 run function rlk:boss/raiden/blink_relocate
execute if score @s rdBlink matches 4 at @s run function rlk:boss/raiden/movement/arrive
execute if score @s rdBlink matches 4 at @s run playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~1 ~ 0.22 1.75 0.1
scoreboard players add @s rdBlink 1
execute if score @s rdBlink matches 10.. run scoreboard players set @s rdBlink 0
