# the dive shadow on the ground: from the landing point back to under the bird (dark; red once locked)
execute positioned ~-0.5 ~ ~-0.5 if entity @s[dx=0,dy=24,dz=0] run return 0
execute if score #lk tmp matches 0 run particle minecraft:dust{color:[0.13,0.05,0.03],scale:1.7} ~ ~0.08 ~ 0.05 0 0.05 0 1
execute if score #lk tmp matches 1 run particle minecraft:dust{color:[0.85,0.16,0.05],scale:1.7} ~ ~0.08 ~ 0.05 0 0.05 0 1
scoreboard players remove #n tmp 1
execute if score #n tmp matches 1.. positioned ^ ^ ^0.5 run function rlk:cm/rv/line
