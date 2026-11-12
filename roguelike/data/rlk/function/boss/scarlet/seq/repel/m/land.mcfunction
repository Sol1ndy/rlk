# R0 down onto the blade: f 1.95 by tick 6 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^0 ^1.95 if function rlk:boss/scarlet/seq/lib/ok run return run function rlk:mboss/mv/glide {t:6}
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^0 ^2.45 if function rlk:boss/scarlet/seq/lib/ok run return run function rlk:mboss/mv/glide {t:6}
