# @s = the anchor (open, every 20 t): the rim breathes between 0.97 and 1.03 of its size (#riftB room 0 / 1).
scoreboard players operation #riftZid room = @s zid
execute if score #riftB room matches 0 run execute as @e[tag=rlk_rift_rim] if score @s zid = #riftZid room run data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{translation:[0f,1.45f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.9255f,2.9255f,2.9255f],right_rotation:[0f,0f,0f,1f]}}
execute if score #riftB room matches 1 run execute as @e[tag=rlk_rift_rim] if score @s zid = #riftZid room run data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{translation:[0f,1.45f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.1065f,3.1065f,3.1065f],right_rotation:[0f,0f,0f,1f]}}
