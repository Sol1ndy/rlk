$execute store result score #cnt tmp run clear @s $(item)[minecraft:custom_data~{rlk:{id:"$(id)"}}] 0
$scoreboard players operation @s it_$(id) = #cnt tmp
# 강화 단계 (#enh, 0~3)
$scoreboard players operation #enh tmp = $(id) enhL
