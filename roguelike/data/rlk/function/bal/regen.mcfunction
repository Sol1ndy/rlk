scoreboard players add @s bal 1
execute if score @s bal >= @s balMax run scoreboard players operation @s bal = @s balMax
execute if score @s balC matches 1 run scoreboard players operation @s balT = #rs1 bal
execute if score @s balC matches 2 run scoreboard players operation @s balT = #rs2 bal
execute if score @s balC matches 3 run scoreboard players operation @s balT = #rs3 bal
execute if score @s bal = @s balMax run scoreboard players set @s balT 0
scoreboard players set @s balF 0
function rlk:bal/ui/draw
