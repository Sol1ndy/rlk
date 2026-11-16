# E16 the walk-in to 4.5 b (0.075 b/t) (@s = the body).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] positioned ^0 ^0 ^4.5 if function rlk:boss/scarlet/seq/lib/ok run return run function rlk:mboss/mv/glide {t:60}
execute at @e[type=minecraft:marker,tag=rlk_hr_stage2,limit=1] positioned ^0 ^0 ^5.5 if function rlk:boss/scarlet/seq/lib/ok run return run function rlk:mboss/mv/glide {t:60}
