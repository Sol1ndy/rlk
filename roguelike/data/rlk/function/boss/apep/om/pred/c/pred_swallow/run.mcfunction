# pred clip pred_swallow (id 22): 24 t, then pred_bud. @s = the husk; apOC = the tick to apply now.
execute if score @s apOC matches 24.. run return run function rlk:boss/apep/om/pred/c/pred_bud/enter
execute if score @s apOC matches ..9 run return run function rlk:boss/apep/om/pred/c/pred_swallow/b/0_9
function rlk:boss/apep/om/pred/c/pred_swallow/b/10_23
