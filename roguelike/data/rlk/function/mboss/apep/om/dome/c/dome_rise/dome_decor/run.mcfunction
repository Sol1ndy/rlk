# dome clip dome_rise (id 41) on dome_decor: 10 t, then dome_idle. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 10.. run return run function rlk:mboss/apep/om/dome/c/dome_idle/dome_decor/enter
execute if score @s apOC matches ..3 run return run function rlk:mboss/apep/om/dome/c/dome_rise/dome_decor/b/0_3
function rlk:mboss/apep/om/dome/c/dome_rise/dome_decor/b/4_8
