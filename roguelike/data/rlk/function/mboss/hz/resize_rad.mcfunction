execute if score @s mbHzR0 matches ..-1 run scoreboard players set @s mbHzR0 0
scoreboard players operation #t mb = @s mbHzR
scoreboard players add #t mb 300
scoreboard players operation @s mbHzRR = #t mb
scoreboard players operation @s mbHzRR *= #t mb
scoreboard players operation #t mb = @s mbHzR0
scoreboard players remove #t mb 300
execute if score #t mb matches ..-1 run scoreboard players set #t mb 0
scoreboard players operation @s mbHzRI = #t mb
scoreboard players operation @s mbHzRI *= #t mb
execute if score @s mbHzK matches 5 run scoreboard players operation @s mbHzRI = @s mbHzR0
execute if score @s mbHzK matches 5 run scoreboard players operation @s mbHzRI *= @s mbHzR0
