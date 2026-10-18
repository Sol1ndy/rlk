# Hook uninstall (no executor; rlk:uninstall via the framework, for every module): the rig, its props, the
# rig objectives the manifest names, every module entity, the module storage, the fx kit (cards, objectives
# fk*, the #fk* fake players, storage rlk:fgkit, its schedules; its stub rig while it has one); the framework
# removes mb, the rlk_mb_aux entities and the low-gravity modifiers (mboss/uninstall -> mboss/lowg_rem).
function rlk:mboss/fieldgen/rig_stub/kill
function rlk:mboss/fieldgen/rig_stub/prop/clear
function rlk:mboss/fieldgen/fx/uninstall
kill @e[tag=rlk_mb_fg_pat]
kill @e[tag=rlk_mb_fg_fx]
kill @e[type=minecraft:marker,tag=rlk_mb_fg_kept]
data remove storage rlk:mboss fg
scoreboard objectives remove fgRigC
scoreboard objectives remove fgRigT
scoreboard objectives remove fgRigF
scoreboard objectives remove fgRigL
scoreboard objectives remove fgRigK
scoreboard objectives remove fgRigY
scoreboard objectives remove fgRigV
