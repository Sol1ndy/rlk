# pred clip pred_swallow (id 22): 24 t, then pred_bud. @s = the husk; apOC = the tick to apply now.
execute if score @s apOC matches 24.. run return run function rlk:mboss/apep/om/pred/c/pred_bud/enter
execute if score @s apOC matches ..10 run return run function rlk:mboss/apep/om/pred/c/pred_swallow/b/0_10
function rlk:mboss/apep/om/pred/c/pred_swallow/b/11_23
