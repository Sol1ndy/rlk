attribute @s minecraft:attack_damage base set 0
attribute @s minecraft:movement_speed base set 0
scoreboard players operation @s mlv = #mbLv mb
execute unless score @s mlv matches 1.. run scoreboard players set @s mlv 1
function rlk:mob/setup
attribute @s minecraft:knockback_resistance base set 1
attribute @s minecraft:explosion_knockback_resistance base set 1
scoreboard players operation @s mhpM = #auxHp mb
scoreboard players operation @s mhpC = #auxHp mb
scoreboard players operation @s mres = #auxRes mb
