$execute store result score #cnt tmp run clear @s $(item)[minecraft:custom_data~{rlk:{id:"$(id)"}}] 0
$scoreboard players operation @s it_$(id) = #cnt tmp
