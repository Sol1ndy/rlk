# The per-tick clip step of any organism husk (dispatch on apK). @s = the husk.
execute if score @s apK matches 1 run return run function rlk:mboss/apep/om/basic/tick
execute if score @s apK matches 2 run return run function rlk:mboss/apep/om/nurt/tick
execute if score @s apK matches 3 run return run function rlk:mboss/apep/om/guard/tick
execute if score @s apK matches 4 run return run function rlk:mboss/apep/om/nest/tick
execute if score @s apK matches 5 run return run function rlk:mboss/apep/om/destr/tick
execute if score @s apK matches 6 run return run function rlk:mboss/apep/om/pred/tick
