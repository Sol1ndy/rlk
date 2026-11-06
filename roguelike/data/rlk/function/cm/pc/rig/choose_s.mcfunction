execute if score @s cmS matches 1 run scoreboard players set #c2p tmp 20
execute if score @s cmS matches 2 run scoreboard players set #c2p tmp 22
execute if score @s cmS matches 2 if score @s cmT matches 9.. run scoreboard players set #c2p tmp 21
execute if score @s cmS matches 3 run scoreboard players set #c2p tmp 30
execute if score @s cmS matches 4 run scoreboard players set #c2p tmp 32
execute if score @s cmS matches 4 if score @s cmT matches 6.. run scoreboard players set #c2p tmp 31
execute if score @s cmS matches 5 run scoreboard players set #c2p tmp 40
execute if score @s cmS matches 6 run scoreboard players set #c2p tmp 44
execute if score @s cmS matches 6 if score @s cmT matches 7.. run scoreboard players set #c2p tmp 41
execute if score @s cmS matches 6 if score @s cmT matches 5..6 run scoreboard players set #c2p tmp 42
execute if score @s cmS matches 6 if score @s cmT matches 3..4 run scoreboard players set #c2p tmp 43
execute if score @s cmS matches 7 run function rlk:cm/pc/rig/heatf
