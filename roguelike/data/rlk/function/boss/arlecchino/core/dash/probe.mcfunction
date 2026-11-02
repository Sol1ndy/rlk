# Dash probe (@s = body, rotated as it): a marker rlk_kn_dp walks forward in 0.5 b steps while the next spot passes
# mv/ok (inside the arena safe disc - 0.5 b, feet and head free), at most #t kn steps; #t2 kn = steps taken.
kill @e[type=minecraft:marker,tag=rlk_kn_dp]
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_dp"]}
execute at @s rotated as @s rotated ~ 0 as @e[type=minecraft:marker,tag=rlk_kn_dp,limit=1] run tp @s ~ ~ ~ ~ 0
scoreboard players set #t2 kn 0
execute as @e[type=minecraft:marker,tag=rlk_kn_dp,limit=1] at @s run function rlk:boss/arlecchino/core/dash/step
