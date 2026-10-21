# nest clip nest_blink (id 14): 6 t, then nest_fly. @s = the husk; apOC = the tick to apply now.
execute if score @s apOC matches 6.. run return run function rlk:mboss/apep/om/nest/c/nest_fly/enter
execute if score @s apOC matches 0 run return run function rlk:mboss/apep/om/nest/c/nest_blink/k/0
execute if score @s apOC matches 1 run return run function rlk:mboss/apep/om/nest/c/nest_blink/k/1
execute if score @s apOC matches 2 run return run function rlk:mboss/apep/om/nest/c/nest_blink/k/2
execute if score @s apOC matches 3 run return run function rlk:mboss/apep/om/nest/c/nest_blink/k/3
execute if score @s apOC matches 4 run return run function rlk:mboss/apep/om/nest/c/nest_blink/k/4
execute if score @s apOC matches 5 run return run function rlk:mboss/apep/om/nest/c/nest_blink/k/5
