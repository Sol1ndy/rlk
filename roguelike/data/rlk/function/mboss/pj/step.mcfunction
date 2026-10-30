execute if score @s mbPjW matches 1 unless block ^ ^ ^0.25 #rlk:cm_pass run return run scoreboard players set #pjStop mb 1
tp @s ^ ^ ^0.25
execute if score @s mbPjHit matches 0 if score @s mbPjD matches 1.. if score @s mbPjK matches 1 at @s run function rlk:mboss/pj/br with storage rlk:mboss pjp
execute if score @s mbPjHit matches 0 if score @s mbPjD matches 1.. unless score @s mbPjK matches 1 at @s run function rlk:mboss/pj/hr with storage rlk:mboss pjp
execute if score #pjStop mb matches 2 run return 0
scoreboard players remove #pjN mb 1
execute if score #pjN mb matches 1.. at @s rotated as @s run function rlk:mboss/pj/step
