# @s = enemy, at @s: the groggy ends, the gauge is full again and the family resumes the enemy
scoreboard players set @s grgT 0
tag @s remove rlk_bal_grog
scoreboard players operation @s bal = @s balMax
scoreboard players set @s balT 0
scoreboard players set @s balF 0
execute if score @s balC matches 3 if entity @s[tag=rlk_mb_body] run function rlk:mboss/d/bal_off
execute if score @s balC matches 3 if entity @s[tag=rlk_raiden] run function rlk:boss/raiden/bal_off
execute if score @s balC matches 1..2 if entity @s[tag=rlk_cmb] run function rlk:bal/fam/cm_off
execute if score @s balC matches 1..2 unless entity @s[tag=rlk_cmb] run function rlk:bal/fam/va_off
playsound minecraft:block.beacon.power_select hostile @a ~ ~ ~ 0.5 1.6
function rlk:bal/ui/draw
