# E2 the lunge to f 3.5 (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^0 ^3.5 if function rlk:boss/scarlet/seq/lib/ok run return run function rlk:mboss/mv/glide {t:4}
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^0 ^4 if function rlk:boss/scarlet/seq/lib/ok run return run function rlk:mboss/mv/glide {t:4}
