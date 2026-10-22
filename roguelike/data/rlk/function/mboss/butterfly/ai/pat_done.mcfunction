# From p/finish: the owner continues. (#bfPRel, set by g.release(), only hides the pattern bar: no butterfly
# state moves on at a release, so returning early here froze the AI for the rest of the fight; review fix S2.)
execute if score #bfPDone mb matches 20 run return run function rlk:mboss/butterfly/form/transform_done
execute if score #bfPDone mb matches 15 run return run function rlk:mboss/butterfly/groggy/begin
function rlk:mboss/butterfly/ai/recover
