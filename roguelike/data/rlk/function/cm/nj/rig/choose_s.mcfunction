execute if score @s cmS matches 1 run scoreboard players set #c2p tmp 20
execute if score @s cmS matches 2 run scoreboard players set #c2p tmp 22
execute if score @s cmS matches 2 if score @s cmT matches 9.. run scoreboard players set #c2p tmp 21
execute if score @s cmS matches 2 if score @s cmAR matches 1.. run scoreboard players set #c2p tmp 20
execute if score @s cmAR matches 1.. run scoreboard players remove @s cmAR 1
execute if score @s cmS matches 3 run scoreboard players set #c2p tmp 24
execute if score @s cmS matches 3 if score @s cmT matches 3.. run scoreboard players set #c2p tmp 23
execute if score @s cmS matches 4 run function rlk:cm/nj/rig/tiredf
execute if score @s cmS matches 5 run scoreboard players set #c2p tmp 40
execute if score @s cmS matches 6 run scoreboard players set #c2p tmp 41
