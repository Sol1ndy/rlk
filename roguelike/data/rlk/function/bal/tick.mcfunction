# @s = enemy, at @s (mob/tick while balT >= 1; Raiden runs bal/boss/tick from her own tick): groggy countdown, else the
# flash and the regen. A registry boss only while its fight runs (#mbSt 1, not paused: the clocks stop with the fight).
execute if score @s balC matches 3 run return run function rlk:bal/boss/tick_mob
execute if score @s grgT matches 1.. run return run function rlk:bal/grog/tick
function rlk:bal/regen_tick
