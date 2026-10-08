# @s = 반응이 일어난 몹
execute store result score @s erodeEnd run time query gametime
scoreboard players operation @s erodeEnd += #erodeDur tmp
