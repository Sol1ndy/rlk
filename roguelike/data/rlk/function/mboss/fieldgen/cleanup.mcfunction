# Hook cleanup (no executor; idempotent; fight end, abort, run end, map change, wipe, uninstall): module
# fake players back to their defaults (the meter, the field, low gravity: the framework's player_reset clears
# #mbLowG, rlk:tick removes the modifiers), the module's storage, every kit card and the kit's HUD flags
# (meter, low gravity, groggy), the field banner if it still shows. Module entities carry rlk_mb_aux.
function rlk:mboss/fieldgen/hud/banner_cut
function rlk:mboss/fieldgen/ai/vars
data remove storage rlk:mboss fg
function rlk:mboss/fieldgen/fx/clear
function rlk:mboss/fieldgen/fx/hud/clear
