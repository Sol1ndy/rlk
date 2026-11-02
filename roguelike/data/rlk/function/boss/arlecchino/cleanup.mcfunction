# Hook cleanup (no executor; idempotent; won / cancel / defeat): every state, hazard and marker of the module, her
# bond taken back (min(bol, #given)), the kit cards and HUD, the rig, the module scores (init makes them again),
# storage core.*.
function rlk:boss/arlecchino/core/stop_all
function rlk:boss/arlecchino/seq/death/cancel
function rlk:boss/arlecchino/seq/intro/cancel
function rlk:boss/arlecchino/seq/t_p2/cancel
function rlk:boss/arlecchino/bond/cleanup
function rlk:boss/arlecchino/fx/clear
function rlk:boss/arlecchino/fx/hud/clear
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/arlecchino/rig/kill
kill @e[tag=rlk_kn_part]
kill @e[tag=rlk_kn_prop]
kill @e[tag=rlk_kn_p]
kill @e[type=minecraft:item,tag=rlk_kn_orb]
kill @e[tag=rlk_kn_wisp]
kill @e[type=minecraft:item_display,tag=rlk_kn_fxf]
scoreboard players set #mbBolRe mb 100
scoreboard players reset * kn
data remove storage rlk:kn core
data remove storage rlk:kn p2
