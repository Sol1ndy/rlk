# pred clip pred_bite (id 26): 6 t, then pred_swim. @s = the husk; apOC = the tick to apply now.
execute if score @s apOC matches 6.. run return run function rlk:boss/apep/om/pred/c/pred_swim/enter
execute if score @s apOC matches 0 run return run function rlk:boss/apep/om/pred/c/pred_bite/k/0
execute if score @s apOC matches 2 run return run function rlk:boss/apep/om/pred/c/pred_bite/k/2
execute if score @s apOC matches 3 run return run function rlk:boss/apep/om/pred/c/pred_bite/k/3
execute if score @s apOC matches 4 run return run function rlk:boss/apep/om/pred/c/pred_bite/k/4
execute if score @s apOC matches 5 run return run function rlk:boss/apep/om/pred/c/pred_bite/k/5
