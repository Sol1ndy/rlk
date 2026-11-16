# 양육 (nurt): the current clip (apOI) at tick apOC. @s = the husk.
execute if score @s apOI matches 6 run return run function rlk:boss/apep/om/nurt/c/nurt_idle/run
execute if score @s apOI matches 7 run return run function rlk:boss/apep/om/nurt/c/nurt_buff/run
execute if score @s apOI matches 8 run return run function rlk:boss/apep/om/nurt/c/nurt_die/run
