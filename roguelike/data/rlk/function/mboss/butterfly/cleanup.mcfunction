# Hook cleanup (no executor; idempotent; fight end, abort, run end, map change, wipe, uninstall): module
# fake players back to their defaults, 달빛 고치 / 달빛 축복 받음 off, every kit card and both kit HUD badges
# gone. Module entities carry rlk_mb_aux.
function rlk:mboss/butterfly/ai/vars
function rlk:mboss/butterfly/fx/clear
function rlk:mboss/butterfly/fx/hud/clear
