# Q lunge probe step (@s = the probe, at / rotated as it): 0.5 b on while mv/ok passes, until within 2 b of the lock.
execute if score #t2 hr >= #t hr run return 0
execute if entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1,distance=..2.0] run return 0
execute positioned ^ ^ ^0.5 unless function rlk:mboss/mv/ok run return 0
tp @s ^ ^ ^0.5
scoreboard players add #t2 hr 1
execute at @s run function rlk:boss/scarlet/p/q/lstep
