# fight_tick of a boss whose gauge is not idle: regen / groggy clock / pending groggy, then the module's bal_tick
# INSTEAD of its tick while groggy (mboss_lib.BAL_HOOKS), else the usual tick and leash.
function rlk:bal/boss/tick
execute if score @s grgT matches 1.. run return run function rlk:mboss/d/bal_tick
function rlk:mboss/d/tick
execute if score #mbSt mb matches 1 unless score #mbNoLeash mb matches 1 run function rlk:mboss/mv/leash
