# One probe step (@s = the probe marker, at / rotated as it).
execute if score #t2 kn >= #t kn run return 0
execute positioned ^ ^ ^0.5 unless function rlk:mboss/mv/ok run return 0
tp @s ^ ^ ^0.5
scoreboard players add #t2 kn 1
execute at @s run function rlk:boss/arlecchino/core/dash/step
