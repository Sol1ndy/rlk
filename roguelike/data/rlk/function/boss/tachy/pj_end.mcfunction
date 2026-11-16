# Hook pj_end (@s = a projectile prop, #pjEv; #pjKeep preset): the pattern that launched it, if it has a pj_end.
execute if entity @s[tag=rlk_tk_p_w1] run return run function rlk:boss/tachy/p/w1/pj_end
execute if entity @s[tag=rlk_tk_p_w2] run return run function rlk:boss/tachy/p/w2/pj_end
execute if entity @s[tag=rlk_tk_p_mantle] run return run function rlk:boss/tachy/p/mantle/pj_end
