# @s = normal / elite enemy, at @s (mob/tick while balT >= 1): groggy countdown, else the flash and the regen
execute if score @s grgT matches 1.. run return run function rlk:bal/grog/tick
function rlk:bal/regen_tick
