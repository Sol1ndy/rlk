# Hook uninstall (no executor; every enabled module): the kit, the rig, every rlk_hr_* entity, objective hr (incl. the
# event scores), storage rlk:hr.
function rlk:boss/scarlet/rig_stub/uninstall
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
scoreboard objectives remove hr
data remove storage rlk:hr core
data remove storage rlk:hr ev
data remove storage rlk:hr fx
data remove storage rlk:hr g
data remove storage rlk:hr rig
data remove storage rlk:hr seq
