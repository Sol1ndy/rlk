# @s = an enemy set up again (mob/setup): the gauge stays; a normal / elite whose row went with its old head bar gets one
execute unless score @s balC matches 1..2 run return 0
scoreboard players set #has bal 0
execute on passengers if entity @s[tag=rlk_hb_bal] run scoreboard players set #has bal 1
execute if score #has bal matches 0 run function rlk:bal/ui/row_new
function rlk:bal/ui/draw
