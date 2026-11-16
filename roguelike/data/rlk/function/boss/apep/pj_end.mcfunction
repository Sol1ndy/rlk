# Hook pj_end (@s = prop, #pjEv, #pjKeep): routed by the prop's pattern tag rlk_mb_ap_p<id> (organisms: rlk_mb_ap_opj).
execute if entity @s[tag=rlk_mb_ap_p3] run return run function rlk:boss/apep/p/glow/pj_end
execute if entity @s[tag=rlk_mb_ap_opj] run return run function rlk:boss/apep/org/pj_end
