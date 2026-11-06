# dome clip dome_idle (id 42) on dome_decor: 40 t, loop. @s = the display; apOC = the tick to apply now.
execute if score @s apOC matches 40.. run scoreboard players set @s apOC 0
execute if score @s apOC matches 0 run return run function rlk:boss/apep/om/dome/c/dome_idle/dome_decor/k/0
