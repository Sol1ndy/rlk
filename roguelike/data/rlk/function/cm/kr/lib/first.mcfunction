# first brain tick: the 1-level HP (70) and no vanilla attack, whatever the room init left in #mhp / #mad
scoreboard players set @s c2eQ 1
scoreboard players set @s mhp0 70
execute unless score @s mlv matches 1.. run scoreboard players set @s mlv 1
function rlk:mob/level_apply
attribute @s minecraft:attack_damage base set 0
