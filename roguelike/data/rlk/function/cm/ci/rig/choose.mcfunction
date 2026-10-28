scoreboard players add @s cmAF 1
execute if score @s cmAF matches 6.. run scoreboard players set @s cmAF 0
scoreboard players operation #c2p tmp = @s cmAF
scoreboard players operation #c2p tmp /= #3 tmp
execute if score @s cmS matches 1 run scoreboard players set #c2p tmp 2
execute if score @s cmS matches 2 run scoreboard players set #c2p tmp 3
