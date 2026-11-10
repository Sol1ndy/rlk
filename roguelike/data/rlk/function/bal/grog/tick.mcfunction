# @s = groggy normal / elite enemy, at @s (bal/tick)
scoreboard players remove @s grgT 1
execute if score @s grgT matches ..0 run return run function rlk:bal/grog/end
scoreboard players operation #m bal = @s grgT
scoreboard players set #k bal 16
scoreboard players operation #m bal %= #k bal
scoreboard players operation #e bal = #m bal
scoreboard players set #k bal 2
scoreboard players operation #e bal %= #k bal
execute if score #e bal matches 0 on passengers if entity @s[tag=rlk_hb_bal] at @s run function rlk:bal/fx/dizzy
