# @s = 플레이어. 방어막이 #dmgIn 을 먼저 흡수. 맞은 원소(#elem)가 방어막 원소(shieldEl)와 같으면 #shElEff%(250%) 효율
execute unless score @s shieldHP matches 1.. run return 0
execute unless score #dmgIn tmp matches 1.. run return 0
execute if score @s shieldEl matches 1.. if score #elem tmp = @s shieldEl run return run function rlk:element/shield_absorb_el
scoreboard players operation #ab tmp = @s shieldHP
execute if score #dmgIn tmp < #ab tmp run scoreboard players operation #ab tmp = #dmgIn tmp
scoreboard players operation @s shieldHP -= #ab tmp
scoreboard players operation #dmgIn tmp -= #ab tmp
execute at @s unless score #k34 snd matches 1 run function rlk:snd/f36
execute unless score @s shieldHP matches 1.. run scoreboard players set @s shieldT 0
