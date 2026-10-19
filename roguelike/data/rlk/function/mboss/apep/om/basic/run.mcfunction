# 기본 (basic): the current clip (apOI) at tick apOC. @s = the husk.
execute if score @s apOI matches 0 run return run function rlk:mboss/apep/om/basic/c/org_spawn/run
execute if score @s apOI matches 1 run return run function rlk:mboss/apep/om/basic/c/basic_bob/run
execute if score @s apOI matches 2 run return run function rlk:mboss/apep/om/basic/c/basic_melee/run
execute if score @s apOI matches 3 run return run function rlk:mboss/apep/om/basic/c/basic_lie/run
execute if score @s apOI matches 4 run return run function rlk:mboss/apep/om/basic/c/basic_ranged/run
execute if score @s apOI matches 5 run return run function rlk:mboss/apep/om/basic/c/org_die/run
