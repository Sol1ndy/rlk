# @s = a camera stand placed on a stage eye point and pulled into the walk disc: when the actor stands with its back
# at the wall, an eye meant to be behind it lands on it. A lens nearer than 1 b (on the floor plane) to the stage
# origin = the actor's place goes 2.5 b over the floor: over its head (the caller aims it afterwards).
execute at @s positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_hr_stage,distance=..1] run return run tp @s ~ 203.5 ~
execute at @s positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_hr_stage2,distance=..1] run return run tp @s ~ 203.5 ~
