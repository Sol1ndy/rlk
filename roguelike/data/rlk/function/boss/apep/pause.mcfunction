# Hook pause (the fight froze): the kit's telegraphs and overlays go; every active pattern's pause; phase 2:
# the walls are cleared (re-cast later) and the organisms freeze (the module tick does not run; plan 7.2).
function rlk:boss/apep/fx/tele/clear
function rlk:boss/apep/fx/hud/flash_end
function rlk:boss/apep/fx/hud/banner_end
function rlk:boss/apep/p/pause_d
execute if score #apPh mb matches 2 run function rlk:boss/apep/rev/pause
