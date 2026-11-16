# @s = enemy, #n bal = pips to take. Returns 1 when taken; fails without a gauge, while groggy / pending, or when the
# enemy refuses balance damage now (bosses: intro, death, cutscene, hidden bars; Raiden: see bal/boss/may).
execute unless score @s balMax matches 1.. run return fail
execute if score @s grgT matches 1.. run return fail
execute if entity @s[tag=rlk_bal_pend] run return fail
execute unless score #n bal matches 1.. run return fail
execute if score @s balC matches 3 unless function rlk:bal/boss/may run return fail
scoreboard players operation @s bal -= #n bal
execute if score @s bal matches ..-1 run scoreboard players set @s bal 0
execute if score @s balC matches 1 run scoreboard players operation @s balT = #rd1 bal
execute if score @s balC matches 2 run scoreboard players operation @s balT = #rd2 bal
execute if score @s balC matches 3 run scoreboard players operation @s balT = #rd3 bal
scoreboard players operation @s balF = #flash bal
execute if score @s bal matches 0 run function rlk:bal/grog/try
execute unless score @s grgT matches 1.. run function rlk:bal/ui/draw
return 1
