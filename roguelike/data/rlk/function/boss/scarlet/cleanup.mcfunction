# Hook cleanup (no executor; idempotent; won / cancel / defeat / map change): every state, hazard and marker of the
# module, the kit cards and HUD, the rig, every rlk_hr_* entity, every fake player of objective hr (init / spawn make
# them again) and storage core.* / seq.*. Never the event scores (api.EV_FP, saved around `reset *`) nor ev.*: the
# reward hook reads them after this. The framework flags of the module go too: #mbNpOwn (her own flashes) and
# #mbBalOff (FN-bal).
function rlk:boss/scarlet/core/stop_all
scoreboard players set #mbNpOwn mb 0
scoreboard players set #mbBalOff mb 0
function rlk:boss/scarlet/seq/intro/cancel
function rlk:boss/scarlet/seq/cs1/cancel
function rlk:boss/scarlet/seq/lead60/cancel
function rlk:boss/scarlet/seq/repel/cancel
function rlk:boss/scarlet/seq/lead5/cancel
function rlk:boss/scarlet/seq/lead_re/cancel
function rlk:boss/scarlet/seq/ending/cancel
function rlk:boss/scarlet/seq/event/cancel
function rlk:boss/scarlet/fx/clear
function rlk:boss/scarlet/fx/hud/clear
function rlk:boss/scarlet/fx/hud/warn {on:0}
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/scarlet/rig/kill
kill @e[tag=rlk_hr_a9s]
kill @e[tag=rlk_hr_anchor]
kill @e[tag=rlk_hr_cut]
kill @e[tag=rlk_hr_deco]
kill @e[tag=rlk_hr_deco_lotus]
kill @e[tag=rlk_hr_deco_moon_halo]
kill @e[tag=rlk_hr_deco_seat_rock]
kill @e[tag=rlk_hr_down]
kill @e[tag=rlk_hr_dp]
kill @e[tag=rlk_hr_ev]
kill @e[tag=rlk_hr_fx]
kill @e[tag=rlk_hr_lock]
kill @e[tag=rlk_hr_near]
kill @e[tag=rlk_hr_p]
kill @e[tag=rlk_hr_part]
kill @e[tag=rlk_hr_pip]
kill @e[tag=rlk_hr_pl8]
kill @e[tag=rlk_hr_shadow]
kill @e[tag=rlk_hr_stage]
tag @e[tag=rlk_hr_ghost] remove rlk_hr_ghost
scoreboard players add #hrEv hr 0
scoreboard players add #hrEvDone hr 0
scoreboard players add #hrEvDrop hr 0
scoreboard players operation #hrEvK tmp = #hrEv hr
scoreboard players operation #hrEvDoneK tmp = #hrEvDone hr
scoreboard players operation #hrEvDropK tmp = #hrEvDrop hr
scoreboard players reset * hr
scoreboard players operation #hrEv hr = #hrEvK tmp
scoreboard players operation #hrEvDone hr = #hrEvDoneK tmp
scoreboard players operation #hrEvDrop hr = #hrEvDropK tmp
scoreboard players reset #hrEvK tmp
scoreboard players reset #hrEvDoneK tmp
scoreboard players reset #hrEvDropK tmp
data remove storage rlk:hr core
data remove storage rlk:hr seq
