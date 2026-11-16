# destr clip destr_blast (id 19): 1 t, holds. @s = the husk; apOC = the tick to apply now.
execute if score @s apOC matches 2.. run return run scoreboard players set @s apOC 2
execute if score @s apOC matches 0 run return run function rlk:boss/apep/om/destr/c/destr_blast/k/0
execute if score @s apOC matches 1 run return run function rlk:boss/apep/om/destr/c/destr_blast/k/1
