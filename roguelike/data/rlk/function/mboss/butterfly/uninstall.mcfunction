# Hook uninstall (no executor; rlk:uninstall via the framework, for every module): the rig, its props, the
# rig objectives the manifest names, the fx kit (cards, objectives bk*, storage rlk:bfkit, its scheduled
# ager); the framework removes mb and the rlk_mb_aux entities.
function rlk:mboss/butterfly/rig_stub/kill
function rlk:mboss/butterfly/rig_stub/prop/clear
function rlk:mboss/butterfly/fx/uninstall
kill @e[type=minecraft:item_display,tag=rlk_mb_bf_dew]
kill @e[tag=rlk_mb_bf_fx]
scoreboard objectives remove bfStubC
scoreboard objectives remove bfStubT
scoreboard objectives remove bfStubF
scoreboard objectives remove bfStubL
scoreboard objectives remove bfStubY
