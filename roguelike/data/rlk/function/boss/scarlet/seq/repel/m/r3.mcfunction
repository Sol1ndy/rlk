# R3 the half circle, leg 3 of 8 (@s = the body; candidates in order, checked with mv/ok; none passes: she stays).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^-1.143 ^ ^0.474 positioned ~ 201.924 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:2}
