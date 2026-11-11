# hr_design §1.3: after repel {at:60} (@s = body): balance + 3 pips (at most her maximum; the video's
# single refill). Nothing while a groggy runs or without a gauge.
execute unless score @s balMax matches 1.. run return 0
execute if score @s grgT matches 1.. run return 0
scoreboard players add @s bal 3
execute if score @s bal > @s balMax run scoreboard players operation @s bal = @s balMax
execute if score @s bal >= @s balMax run scoreboard players set @s balT 0
function rlk:bal/ui/draw
