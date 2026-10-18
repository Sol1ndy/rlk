# The core bubble shows the next crack stage (#fgCrack, read by reloads and tests). The kit's meter_hit
# cracks its own stub rig (rlk:mboss/fieldgen/fx/rig_stub/) while the real rig is not merged, so the core cracks its rig here.
scoreboard players operation #fgCrack mb = #fgX mb
function rlk:mboss/fieldgen/u/crack_d
