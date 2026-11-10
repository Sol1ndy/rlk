# @s = boss body, at @s (mob/tick -> bal/tick -> boss/tick_mob for a registry boss, boss/raiden/tick for Raiden, while
# balT >= 1; a paused fight does not run it)
execute if entity @s[tag=rlk_bal_pend] run return run function rlk:bal/boss/pend_tick
execute if score @s grgT matches 1.. run return run function rlk:bal/boss/grog_tick
function rlk:bal/regen_tick
