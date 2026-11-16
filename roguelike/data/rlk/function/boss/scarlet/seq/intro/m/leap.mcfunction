# I16 the leap to f 6.5 (apex 4.5 b) (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^0 ^6.5 if function rlk:boss/scarlet/seq/lib/ok run return run function rlk:mboss/mv/leap {t:24,h:45}
