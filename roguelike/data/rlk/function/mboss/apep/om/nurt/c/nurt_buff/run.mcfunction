# nurt clip nurt_buff (id 7): 20 t, then nurt_idle. @s = the husk; apOC = the tick to apply now.
execute if score @s apOC matches 20.. run return run function rlk:mboss/apep/om/nurt/c/nurt_idle/enter
execute if score @s apOC matches ..9 run return run function rlk:mboss/apep/om/nurt/c/nurt_buff/b/0_9
function rlk:mboss/apep/om/nurt/c/nurt_buff/b/11_19
