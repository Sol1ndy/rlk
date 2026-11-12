# As the boss with a chosen pattern that closes in first (rdGo 1..): the clock stays at 0 until the blink is over.
scoreboard players set @s rdTime 0
scoreboard players add @s rdGo 1
execute if score @s rdGo matches 2 run return run function rlk:boss/raiden/close_blink
execute unless score @s rdBlink matches 1.. run function rlk:boss/raiden/close_done
