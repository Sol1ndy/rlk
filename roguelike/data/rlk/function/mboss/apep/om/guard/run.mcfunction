# 수호 (guard): the current clip (apOI) at tick apOC. @s = the husk.
execute if score @s apOI matches 9 run return run function rlk:mboss/apep/om/guard/c/guard_idle/run
execute if score @s apOI matches 10 run return run function rlk:mboss/apep/om/guard/c/guard_cast/run
execute if score @s apOI matches 11 run return run function rlk:mboss/apep/om/guard/c/guard_die/run
