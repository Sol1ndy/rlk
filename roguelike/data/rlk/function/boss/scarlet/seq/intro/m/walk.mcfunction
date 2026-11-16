# I15 the walk to f 13.5 over 96 t (0.075 b/t) (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^0 ^13.5 if function rlk:boss/scarlet/seq/lib/ok run return run function rlk:mboss/mv/glide {t:96}
