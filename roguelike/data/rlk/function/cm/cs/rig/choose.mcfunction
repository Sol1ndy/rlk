scoreboard players add @s cmAF 1
execute if score @s cmAF matches 24.. run scoreboard players set @s cmAF 0
execute if score @s cmS matches 1.. run return run function rlk:cm/cs/rig/choose_s
scoreboard players operation #c2p tmp = @s cmAF
scoreboard players operation #c2p tmp /= #st6 tmp
execute unless entity @s[tag=rlk_cmhold] unless score @s stunT matches 1.. unless entity @e[tag=rlk_body,distance=..2.4] run function rlk:cm/cs/rig/walkf
execute if score @s cmAH matches 4.. run scoreboard players set #c2p tmp 50
execute if score @s cmAH matches 1..3 run scoreboard players set #c2p tmp 51
