# Dash / leap / blink probe (@s = body, rotated as the direction): the marker rlk_hr_dp walks forward on the floor in
# 0.5 b steps while the next spot passes mv/ok (inside MOVE_R, feet and head free), at most #t steps; #t2 = steps.
kill @e[type=minecraft:marker,tag=rlk_hr_dp]
execute positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_dp"]}
execute as @e[type=minecraft:marker,tag=rlk_hr_dp,limit=1] run tp @s ~ ~ ~ ~ 0
scoreboard players set #t2 hr 0
execute as @e[type=minecraft:marker,tag=rlk_hr_dp,limit=1] at @s run function rlk:boss/scarlet/core/dash/step
