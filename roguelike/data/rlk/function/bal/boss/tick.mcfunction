# @s = boss body, at @s (mboss/fight_tick, boss/raiden/tick while balT >= 1; a paused fight does not run it)
execute if entity @s[tag=rlk_bal_pend] run return run function rlk:bal/boss/pend_tick
execute if score @s grgT matches 1.. run return run function rlk:bal/boss/grog_tick
function rlk:bal/regen_tick
