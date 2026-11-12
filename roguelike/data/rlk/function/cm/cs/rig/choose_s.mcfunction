execute if score @s cmS matches 1 run scoreboard players set #c2p tmp 21
execute if score @s cmS matches 1 if score @s cmT matches 6.. run scoreboard players set #c2p tmp 20
execute if score @s cmS matches 2 run scoreboard players set #c2p tmp 22
execute if score @s cmS matches 3 run function rlk:cm/cs/rig/moundf
execute if score @s cmS matches 4 run function rlk:cm/cs/rig/stuckf
execute if score @s cmS matches 5 run scoreboard players set #c2p tmp 30
execute if score @s cmS matches 6 run scoreboard players set #c2p tmp 31
execute if score @s cmS matches 7 run scoreboard players set #c2p tmp 33
execute if score @s cmS matches 7 if score @s cmT matches 7.. run scoreboard players set #c2p tmp 32
execute if score @s cmS matches 8 run scoreboard players set #c2p tmp 40
execute if score @s cmS matches 9 run scoreboard players set #c2p tmp 42
execute if score @s cmS matches 9 if score @s cmT matches 9.. run scoreboard players set #c2p tmp 41
# a hit shows the recoil only in the punish window (never over a tell pose)
execute if score @s cmS matches 4 if score @s cmT matches ..16 if score @s cmAH matches 4.. run scoreboard players set #c2p tmp 50
