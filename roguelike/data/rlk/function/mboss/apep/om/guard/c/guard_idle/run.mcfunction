# guard clip guard_idle (id 9): 60 t, loop. @s = the husk; apOC = the tick to apply now.
execute if score @s apOC matches 60.. run scoreboard players set @s apOC 0
execute if score @s apOC matches ..25 run return run function rlk:mboss/apep/om/guard/c/guard_idle/b/0_25
function rlk:mboss/apep/om/guard/c/guard_idle/b/26_55
