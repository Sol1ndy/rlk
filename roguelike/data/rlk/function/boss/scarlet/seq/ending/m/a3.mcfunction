# E6 the big one (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^6 ^3.3 if function rlk:boss/scarlet/seq/lib/ok run return run function rlk:mboss/mv/glide {t:10}
