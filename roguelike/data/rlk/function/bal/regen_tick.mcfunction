# @s = enemy with pips missing: the white pip goes back to empty, and after the delay +1 pip per step
execute if score @s balF matches 1.. run function rlk:bal/flash
scoreboard players remove @s balT 1
execute if score @s balT matches ..0 run function rlk:bal/regen
