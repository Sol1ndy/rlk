# @s = enemy, at @s: the groggy starts (tier length); the family stops the enemy cleanly
execute if score @s balC matches 1 run scoreboard players operation @s grgT = #grg1 bal
execute if score @s balC matches 2 run scoreboard players operation @s grgT = #grg2 bal
execute if score @s balC matches 3 run scoreboard players operation @s grgT = #grg3 bal
scoreboard players set @s balT 1
scoreboard players set @s balF 0
scoreboard players set @s bal 0
tag @s add rlk_bal_grog
tag @s remove rlk_bal_pend
function rlk:bal/fx/start
execute if score @s balC matches 3 if entity @s[tag=rlk_mb_body] run function rlk:mboss/d/bal_on
execute if score @s balC matches 3 if entity @s[tag=rlk_raiden] run function rlk:boss/raiden/bal_on
execute if score @s balC matches 1..2 if entity @s[tag=rlk_cmb] run function rlk:bal/fam/cm_on
execute if score @s balC matches 1..2 unless entity @s[tag=rlk_cmb] run function rlk:bal/fam/va_on
function rlk:bal/ui/draw
