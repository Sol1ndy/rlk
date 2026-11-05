# R3 the half circle, leg 1 of 8 (@s = the body; candidates in order, checked with mv/ok; none passes: she stays).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^-0.541 ^ ^1.305 positioned ~ 201.383 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:2}
