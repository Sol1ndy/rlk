# From p/finish: the field sequence moves on; any other pattern recovers. (No early return on a released
# pattern: the butterfly's S2 froze the AI there.)
execute if score #fgPDone mb matches 20 run return run function rlk:mboss/fieldgen/field/opened
execute if score #fgPDone mb matches 21 if score #fgWvK mb matches 1 run return run function rlk:mboss/fieldgen/field/patterns
execute if score #fgPDone mb matches 21 if score #fgWvK mb matches 2 run return run function rlk:mboss/fieldgen/field/packing
execute if score #fgPDone mb matches 22 run return run function rlk:mboss/fieldgen/field/down
function rlk:mboss/fieldgen/ai/recover
