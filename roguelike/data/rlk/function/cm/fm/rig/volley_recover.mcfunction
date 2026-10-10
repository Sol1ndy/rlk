# During the three-shot volley, pull back and ready the next thrust in time for its launch.
execute if score @s cmAR matches 4..7 run scoreboard players set #fmPose tmp 31
execute if score @s cmAR matches 1..3 run scoreboard players set #fmPose tmp 32
