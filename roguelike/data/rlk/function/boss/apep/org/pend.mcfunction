# @s = a pending spawn marker, at it.
scoreboard players add @s apT 1
execute if score @s apT matches ..19 run return 0
scoreboard players operation #apOArg mb = @s apS
execute if score @s apK matches 1 run function rlk:boss/apep/org/spawn_basic
execute if score @s apK matches 2 run function rlk:boss/apep/org/spawn_nurt
execute if score @s apK matches 3 run function rlk:boss/apep/org/spawn_guard
execute if score @s apK matches 4 run function rlk:boss/apep/org/spawn_nest
execute if score @s apK matches 5 run function rlk:boss/apep/org/spawn_destr
execute if score @s apK matches 6 run function rlk:boss/apep/org/spawn_pred
kill @s
