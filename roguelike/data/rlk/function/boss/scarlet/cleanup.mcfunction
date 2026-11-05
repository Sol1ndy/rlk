# Hook cleanup (no executor; idempotent; won / cancel / defeat / map change): every state, hazard and marker of the
# module, the kit cards and HUD, the rig, every rlk_hr_* entity, the core's scores (init / spawn make them again) and
# storage core.*. Never the event scores (api.EV_FP) nor ev.*: the reward hook reads them after this.
function rlk:boss/scarlet/core/stop_all
function rlk:boss/scarlet/seq/intro/cancel
function rlk:boss/scarlet/seq/cs1/cancel
function rlk:boss/scarlet/seq/sq1/cancel
function rlk:boss/scarlet/seq/repel/cancel
function rlk:boss/scarlet/seq/lead_down/cancel
function rlk:boss/scarlet/seq/lead_stand/cancel
function rlk:boss/scarlet/seq/ending/cancel
function rlk:boss/scarlet/seq/event/cancel
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
scoreboard players reset #ph hr
scoreboard players reset #pat hr
scoreboard players reset #pt hr
scoreboard players reset #done hr
scoreboard players reset #clk hr
scoreboard players reset #rigc hr
scoreboard players reset #rigt hr
scoreboard players reset #sq hr
scoreboard players reset #sqdone hr
scoreboard players reset #hud hr
scoreboard players reset #fl hr
scoreboard players reset #tst hr
scoreboard players reset #lock hr
scoreboard players reset #last hr
scoreboard players reset #last2 hr
scoreboard players reset #rear hr
scoreboard players reset #far hr
scoreboard players reset #dec hr
scoreboard players reset #rec hr
scoreboard players reset #hits hr
scoreboard players reset #a6cd hr
scoreboard players reset #pips hr
scoreboard players reset #gres hr
scoreboard players reset #gk hr
scoreboard players reset #down hr
scoreboard players reset #skip hr
scoreboard players reset #warn hr
scoreboard players reset #inv hr
scoreboard players reset #hrLook hr
scoreboard players reset #t hr
scoreboard players reset #t2 hr
scoreboard players reset #t3 hr
scoreboard players reset #t4 hr
scoreboard players reset #t5 hr
scoreboard players reset #cn1 hr
scoreboard players reset #cn1000 hr
scoreboard players reset #c2 hr
scoreboard players reset #c3 hr
scoreboard players reset #c5 hr
scoreboard players reset #c10 hr
scoreboard players reset #c64 hr
scoreboard players reset #c100 hr
scoreboard players reset #c577 hr
scoreboard players reset #c1000 hr
scoreboard players reset #c36000 hr
scoreboard players reset #fl60 hr
scoreboard players reset #fl5 hr
scoreboard players reset #flw hr
scoreboard players reset #sqn hr
scoreboard players reset #sqh hr
scoreboard players reset #shb hr
scoreboard players reset #kip hr
scoreboard players reset #grs hr
scoreboard players reset #rvw hr
scoreboard players reset #a6q hr
scoreboard players reset #ctr hr
scoreboard players reset #flq hr
scoreboard players reset #h1 hr
scoreboard players reset #h2 hr
scoreboard players reset #h3 hr
scoreboard players reset #h4 hr
scoreboard players reset #pipoff hr
scoreboard players reset #lk hr
scoreboard players reset #skp hr
scoreboard players reset #rp hr
scoreboard players reset #ai_d2 hr
scoreboard players reset #ai_mv hr
scoreboard players reset #ai_pht hr
scoreboard players reset #ai_sum hr
scoreboard players reset #ai_r hr
scoreboard players reset #ai_rc hr
scoreboard players reset #ai_ff hr
scoreboard players reset #ai_nx hr
scoreboard players reset #ai_rcd hr
scoreboard players reset #ai_fl hr
scoreboard players reset #ai_lf hr
scoreboard players reset #ai_ls hr
scoreboard players reset #ai_wa1 hr
scoreboard players reset #ai_wa2 hr
scoreboard players reset #ai_wa3 hr
scoreboard players reset #ai_wa4 hr
scoreboard players reset #ai_wa6 hr
scoreboard players reset #ai_wa9 hr
scoreboard players reset #ai_wa10 hr
scoreboard players reset #ai_wr1 hr
scoreboard players reset #ai_wr2 hr
scoreboard players reset #ai_wr3 hr
scoreboard players reset #ai_wa8 hr
scoreboard players reset #ai_wa13 hr
scoreboard players reset #cd_a1 hr
scoreboard players reset #cd_a2 hr
scoreboard players reset #cd_a3 hr
scoreboard players reset #cd_a4 hr
scoreboard players reset #cd_a6 hr
scoreboard players reset #cd_a9 hr
scoreboard players reset #cd_a10 hr
scoreboard players reset #cd_r1 hr
scoreboard players reset #cd_r2 hr
scoreboard players reset #cd_r3 hr
scoreboard players reset #sq_sig hr
data remove storage rlk:hr core
