# BLUE probe step (@s = the probe, at / rotated as it): 0.5 b on while mv/ok passes, at most #t steps; once within
# 0.5 b of the locked spot the cap becomes 4 more steps (2 b beyond it).
execute if score #t2 hr >= #t hr run return 0
execute if entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1,distance=..0.5,tag=!rlk_hr_a9p] run function rlk:boss/scarlet/p/blue/past
execute positioned ^ ^ ^0.5 unless function rlk:mboss/mv/ok run return 0
tp @s ^ ^ ^0.5
scoreboard players add #t2 hr 1
execute at @s run function rlk:boss/scarlet/p/blue/pstep
