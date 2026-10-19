# Hook uninstall (no executor; rlk:uninstall via the framework, for every module): the rig, its props, the
# rig objectives the manifest names, the fx kit (cards, objectives bk*, storage rlk:bfkit, its scheduled
# ager); the framework removes mb and the rlk_mb_aux entities.
function rlk:mboss/butterfly/rig/kill
function rlk:mboss/butterfly/rig/prop/clear
function rlk:mboss/butterfly/fx/uninstall
kill @e[type=minecraft:item_display,tag=rlk_mb_bf_dew]
kill @e[tag=rlk_mb_bf_fx]
# the module's scratch storage (heal-orb spawn args, the decal redraw args; review fix perf-4)
data remove storage rlk:mboss bfd
data remove storage rlk:mboss bfr
scoreboard objectives remove bfRigC
scoreboard objectives remove bfRigT
scoreboard objectives remove bfRigF
scoreboard objectives remove bfRigY
scoreboard objectives remove bfRigForm
scoreboard objectives remove bfRigLook
scoreboard objectives remove bfRigFlat
scoreboard objectives remove bfRigTell
