# @s = aux: #dmg off its own pool (mhpC/mhpM, shown by its overhead bar), number, flash.
execute if score #dmg tmp matches ..0 run return run function rlk:mboss/aux/immune
scoreboard players operation @s mhpC -= #dmg tmp
function rlk:mboss/aux/number
execute if score @s mhpC matches ..0 run function rlk:mboss/aux/broke
