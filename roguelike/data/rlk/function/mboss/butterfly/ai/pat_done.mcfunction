# From p/finish: the owner continues (unless it already moved on at the pattern's release).
execute if score #bfPRel mb matches 1 run return 0
execute if score #bfPDone mb matches 20 run return run function rlk:mboss/butterfly/form/transform_done
execute if score #bfPDone mb matches 15 run return run function rlk:mboss/butterfly/groggy/begin
function rlk:mboss/butterfly/ai/recover
