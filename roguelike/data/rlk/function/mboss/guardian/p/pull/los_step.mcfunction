# One 0.5 b step of the line-of-sight ray (#gp4Ln steps left).
execute unless block ~ ~ ~ #rlk:cm_pass run return run scoreboard players set #gp4Ok mb 0
scoreboard players remove #gp4Ln mb 1
execute if score #gp4Ln mb matches 1.. positioned ^ ^ ^0.5 run function rlk:mboss/guardian/p/pull/los_step
