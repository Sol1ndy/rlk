execute at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] eyes run tp @s ^ ^ ^0.25 ~ ~
# Not 'at <body> anchored eyes': that anchor uses the EXECUTOR's eye height (0 for a display or marker).
execute at @s positioned ~-0.5 ~-0.5 ~-0.5 if entity @e[type=minecraft:husk,tag=rlk_mb_body,dx=0,dy=0,dz=0,limit=1] run return run function rlk:mboss/pj/returned
scoreboard players remove #pjN mb 1
execute if score #pjN mb matches 1.. run function rlk:mboss/pj/back_step
