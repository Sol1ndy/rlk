scoreboard players add @s cmAF 1
execute if score @s cmAF matches 12.. run scoreboard players set @s cmAF 0
scoreboard players operation #c2p tmp = @s cmAF
scoreboard players operation #c2p tmp /= #3 tmp
execute if score @s cmS matches 1 run scoreboard players set #c2p tmp 10
execute if score @s cmS matches 2 run scoreboard players set #c2p tmp 11
execute if score @s cmS matches 3 run scoreboard players set #c2p tmp 12
execute if score @s cmS matches 4 run function rlk:cm/rv/rig/crashf
execute if score @s cmS matches 5 run scoreboard players set #c2p tmp 22
execute if score @s cmS matches 6 run scoreboard players set #c2p tmp 30
execute if score @s cmS matches 7 if score @s cmT matches 5.. run scoreboard players set #c2p tmp 31
# hit recoil only while just flying or crashed (never over a tell pose)
execute if score @s cmS matches 0 if score @s cmAH matches 4.. run scoreboard players set #c2p tmp 50
execute if score @s cmS matches 0 if score @s cmAH matches 1..3 run scoreboard players set #c2p tmp 51
execute if score @s cmS matches 4 if score @s cmAH matches 3.. run scoreboard players set #c2p tmp 52
