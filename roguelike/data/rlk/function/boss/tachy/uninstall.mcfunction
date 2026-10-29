# Hook uninstall (no executor; every enabled module): the kit, the rig, the module entities, objective tk, storage.
function rlk:boss/tachy/fx/uninstall
function rlk:boss/tachy/rig/uninstall
kill @e[tag=rlk_tk_p]
kill @e[tag=rlk_tk_air]
kill @e[tag=rlk_tk_part]
kill @e[tag=rlk_tk_prop]
kill @e[tag=rlk_tk_fx]
scoreboard objectives remove tk
data remove storage rlk:tk core
