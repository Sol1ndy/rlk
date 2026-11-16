execute unless block ~ ~0.8 ~ #rlk:dash_pass run return 0
particle minecraft:dust{color:[0.78,0.55,1.0],scale:1.1} ~ ~ ~ 0.05 0 0.05 0 1
scoreboard players remove #n tmp 1
execute if score #n tmp matches 1.. positioned ^ ^ ^0.5 run function rlk:cm/cs/t_lstep
