# @s = 플레이어. 방어막이 #dmgIn 을 먼저 흡수
execute unless score @s shieldHP matches 1.. run return 0
execute unless score #dmgIn tmp matches 1.. run return 0
scoreboard players operation #ab tmp = @s shieldHP
execute if score #dmgIn tmp < #ab tmp run scoreboard players operation #ab tmp = #dmgIn tmp
scoreboard players operation @s shieldHP -= #ab tmp
scoreboard players operation #dmgIn tmp -= #ab tmp
execute at @s run playsound minecraft:block.amethyst_block.hit master @s ~ ~ ~ 1 0.8
execute unless score @s shieldHP matches 1.. run scoreboard players set @s shieldT 0
