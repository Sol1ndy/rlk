# @s = enemy: the row index (0..max plain, max+1+n flash, 2*max+1 groggy) -> head text / the boss row storage
scoreboard players operation #i bal = @s bal
execute if score @s balF matches 1.. if score @s bal < @s balMax run scoreboard players operation #i bal += @s balMax
execute if score @s balF matches 1.. if score @s bal < @s balMax run scoreboard players add #i bal 1
execute if score @s grgT matches 1.. run scoreboard players operation #i bal = @s balMax
execute if score @s grgT matches 1.. run scoreboard players operation #i bal += @s balMax
execute if score @s grgT matches 1.. run scoreboard players add #i bal 1
execute store result storage rlk:bal a.i int 1 run scoreboard players get #i bal
execute store result storage rlk:bal a.m int 1 run scoreboard players get @s balMax
execute if score @s balC matches 3 run return run function rlk:bal/ui/boss with storage rlk:bal a
execute on passengers if entity @s[tag=rlk_hb_bal] run function rlk:bal/ui/head with storage rlk:bal a
