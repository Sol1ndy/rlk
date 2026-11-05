# R3 the half circle, leg 8 of 8 (@s = the body; candidates in order, checked with mv/ok; none passes: she stays).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^ ^-0.8 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:2}
