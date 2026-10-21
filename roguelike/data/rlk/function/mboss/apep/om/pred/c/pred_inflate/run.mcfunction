# pred clip pred_inflate (id 24): 10 t, then pred_burst. @s = the husk; apOC = the tick to apply now.
execute if score @s apOC matches 10.. run return run function rlk:mboss/apep/om/pred/c/pred_burst/enter
execute if score @s apOC matches ..4 run return run function rlk:mboss/apep/om/pred/c/pred_inflate/b/0_4
function rlk:mboss/apep/om/pred/c/pred_inflate/b/5_8
