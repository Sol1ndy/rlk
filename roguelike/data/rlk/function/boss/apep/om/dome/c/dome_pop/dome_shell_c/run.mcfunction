# dome clip dome_pop (id 43) on dome_shell_c: 6 t, then stops. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 7.. run return run scoreboard players set @s apOI -1
execute if score @s apOC matches 0 run return run function rlk:boss/apep/om/dome/c/dome_pop/dome_shell_c/k/0
execute if score @s apOC matches 1 run return run function rlk:boss/apep/om/dome/c/dome_pop/dome_shell_c/k/1
execute if score @s apOC matches 2 run return run function rlk:boss/apep/om/dome/c/dome_pop/dome_shell_c/k/2
execute if score @s apOC matches 3 run return run function rlk:boss/apep/om/dome/c/dome_pop/dome_shell_c/k/3
execute if score @s apOC matches 4 run return run function rlk:boss/apep/om/dome/c/dome_pop/dome_shell_c/k/4
execute if score @s apOC matches 5 run return run function rlk:boss/apep/om/dome/c/dome_pop/dome_shell_c/k/5
