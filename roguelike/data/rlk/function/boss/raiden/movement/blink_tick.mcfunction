# Core tick, as the boss, while rdBlink 1.. .
execute unless score @s rdBlink matches 1.. run return 0
scoreboard players add @s rdBlink 1
execute if score @s rdBlink matches 6 run function rlk:boss/raiden/movement/blink_land
execute if score @s rdBlink matches 10..19 run scoreboard players set @s rdBlink 0
execute if score @s rdBlink matches 30.. run scoreboard players set @s rdBlink 0
