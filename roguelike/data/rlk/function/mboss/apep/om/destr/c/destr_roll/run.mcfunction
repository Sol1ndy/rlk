# destr clip destr_roll (id 16): 32 t, loop. @s = the husk; apOC = the tick to apply now.
execute if score @s apOC matches 32.. run scoreboard players set @s apOC 0
execute if score @s apOC matches 0 run return run function rlk:mboss/apep/om/destr/c/destr_roll/k/0
execute if score @s apOC matches 1 run return run function rlk:mboss/apep/om/destr/c/destr_roll/k/1
execute if score @s apOC matches 2 run return run function rlk:mboss/apep/om/destr/c/destr_roll/k/2
execute if score @s apOC matches 4 run return run function rlk:mboss/apep/om/destr/c/destr_roll/k/4
execute if score @s apOC matches 14 run return run function rlk:mboss/apep/om/destr/c/destr_roll/k/14
execute if score @s apOC matches 24 run return run function rlk:mboss/apep/om/destr/c/destr_roll/k/24
