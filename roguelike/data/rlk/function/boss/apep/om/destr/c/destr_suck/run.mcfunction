# destr clip destr_suck (id 18): 5 t, then destr_blast. @s = the husk; apOC = the tick to apply now.
execute if score @s apOC matches 5.. run return run function rlk:boss/apep/om/destr/c/destr_blast/enter
execute if score @s apOC matches 0 run return run function rlk:boss/apep/om/destr/c/destr_suck/k/0
execute if score @s apOC matches 2 run return run function rlk:boss/apep/om/destr/c/destr_suck/k/2
execute if score @s apOC matches 3 run return run function rlk:boss/apep/om/destr/c/destr_suck/k/3
execute if score @s apOC matches 4 run return run function rlk:boss/apep/om/destr/c/destr_suck/k/4
