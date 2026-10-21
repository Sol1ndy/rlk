# Hook pause (the fight froze): the kit's telegraphs and overlays go; every active pattern's pause; phase 2:
# the walls are cleared (re-cast later) and the organisms freeze (the module tick does not run; plan 7.2).
function rlk:mboss/apep/kstub/tele/clear
function rlk:mboss/apep/kstub/hud/flash_end
function rlk:mboss/apep/kstub/hud/banner_end
function rlk:mboss/apep/p/pause_d
execute if score #apPh mb matches 2 run function rlk:mboss/apep/rev/pause
