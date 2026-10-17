execute at @s facing entity @e[tag=rlk_mb_body,limit=1] eyes run tp @s ^ ^ ^0.25 ~ ~
execute at @s if entity @e[tag=rlk_mb_body,distance=..1.5,limit=1] run return run function rlk:mboss/pj/returned
scoreboard players remove #pjN mb 1
execute if score #pjN mb matches 1.. run function rlk:mboss/pj/back_step
