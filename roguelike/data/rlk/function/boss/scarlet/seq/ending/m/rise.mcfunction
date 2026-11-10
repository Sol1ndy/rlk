# E6 up to ST(0, 6.0, 3.6) (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^6 ^3.6 if function rlk:boss/scarlet/seq/lib/ok run return run function rlk:mboss/mv/glide {t:12}
