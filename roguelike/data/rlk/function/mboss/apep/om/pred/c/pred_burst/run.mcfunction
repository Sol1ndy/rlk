# pred clip pred_burst (id 25): 10 t, then pred_swim. @s = the husk; apOC = the tick to apply now.
execute if score @s apOC matches 10.. run return run function rlk:mboss/apep/om/pred/c/pred_swim/enter
execute if score @s apOC matches ..3 run return run function rlk:mboss/apep/om/pred/c/pred_burst/b/0_3
function rlk:mboss/apep/om/pred/c/pred_burst/b/4_8
