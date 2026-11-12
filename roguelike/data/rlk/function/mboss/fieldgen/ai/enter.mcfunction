# Enter idle (#fgCool set by the caller). Idle is never groggy: the kit's " · 그로기" flag goes (recovery
# end, test cuts, reloads).
scoreboard players set #fgSt mb 0
scoreboard players set #fgT mb 0
execute if data storage rlk:fgkit hud{grog:1b} run function rlk:mboss/fieldgen/fx/hud/groggy_off
function rlk:mboss/fieldgen/hud/refresh
