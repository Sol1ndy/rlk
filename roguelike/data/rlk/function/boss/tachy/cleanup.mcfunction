# Hook cleanup (no executor; idempotent): every state, hazard and marker of the module, the kit cards and HUD,
# the rig, the module scores (init makes them again) and storage core.*.
function rlk:boss/tachy/core/stop_all
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/tachy/rig_stub/kill
kill @e[tag=rlk_tk_part]
kill @e[tag=rlk_tk_prop]
kill @e[type=minecraft:marker,tag=rlk_tk_dp]
scoreboard players reset * tk
data remove storage rlk:tk core
