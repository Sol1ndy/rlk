scoreboard players operation #r rvp = #k rvp
scoreboard players operation #r rvp %= #per rvp
scoreboard players add #k rvp 1
execute store result score #now cb run time query gametime
execute if score #r rvp matches 0 run item replace entity @s weapon.offhand with minecraft:stick[minecraft:custom_data={rlk_ui:{role:"attack"}}]
scoreboard players operation @s rvpLast = @s parAt
function rlk:player/def/input
item replace entity @s weapon.offhand with minecraft:air
execute unless score @s rvpLast = @s parAt run scoreboard players add @s rvpAcc 1
execute if score #k rvp matches 240.. run function rvp:a01_end
