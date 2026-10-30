# pred clip pred_bud (id 23): 20 t, loop. @s = the husk; apOC = the tick to apply now.
execute if score @s apOC matches 20.. run scoreboard players set @s apOC 0
execute if score @s apOC matches 0 run return run function rlk:boss/apep/om/pred/c/pred_bud/k/0
execute if score @s apOC matches 1 run return run function rlk:boss/apep/om/pred/c/pred_bud/k/1
execute if score @s apOC matches 2 run return run function rlk:boss/apep/om/pred/c/pred_bud/k/2
execute if score @s apOC matches 5 run return run function rlk:boss/apep/om/pred/c/pred_bud/k/5
execute if score @s apOC matches 10 run return run function rlk:boss/apep/om/pred/c/pred_bud/k/10
execute if score @s apOC matches 15 run return run function rlk:boss/apep/om/pred/c/pred_bud/k/15
