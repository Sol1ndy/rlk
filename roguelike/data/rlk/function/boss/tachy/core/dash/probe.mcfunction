# Dash probe (@s = body, rotated as it): a marker rlk_tk_dp walks forward in 0.5 b steps while the next spot passes
# mv/ok (inside the arena safe disc - 0.5 b, feet and head free), at most #t tk steps; #t2 tk = steps taken.
kill @e[type=minecraft:marker,tag=rlk_tk_dp]
execute at @s rotated as @s rotated ~ 0 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_p","rlk_tk_dp"]}
execute at @s rotated as @s rotated ~ 0 as @e[type=minecraft:marker,tag=rlk_tk_dp,limit=1] run tp @s ~ ~ ~ ~ 0
scoreboard players set #t2 tk 0
execute as @e[type=minecraft:marker,tag=rlk_tk_dp,limit=1] at @s run function rlk:boss/tachy/core/dash/step
