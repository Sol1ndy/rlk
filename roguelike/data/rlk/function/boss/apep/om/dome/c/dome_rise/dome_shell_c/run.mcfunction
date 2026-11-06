# dome clip dome_rise (id 41) on dome_shell_c: 10 t, then dome_idle. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 10.. run return run function rlk:boss/apep/om/dome/c/dome_idle/dome_shell_c/enter
execute if score @s apOC matches ..3 run return run function rlk:boss/apep/om/dome/c/dome_rise/dome_shell_c/b/0_3
function rlk:boss/apep/om/dome/c/dome_rise/dome_shell_c/b/4_8
