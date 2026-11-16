# guard clip guard_cast (id 10): 30 t, then guard_idle. @s = the husk; apOC = the tick to apply now.
execute if score @s apOC matches 30.. run return run function rlk:boss/apep/om/guard/c/guard_idle/enter
execute if score @s apOC matches ..15 run return run function rlk:boss/apep/om/guard/c/guard_cast/b/0_15
function rlk:boss/apep/om/guard/c/guard_cast/b/16_28
