# The gap-closer spot (@s = body): around the player (its facing) - behind, then the back / front diagonals and the
# sides (a random side first), the front last, 2.6 b then 3.4 b; each must pass mv/ok; else she stays.
execute store result score #cl_r tk run random value 0..1
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~180 0 positioned ^ ^ ^2.6 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 0 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~135 0 positioned ^ ^ ^2.6 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 0 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~-135 0 positioned ^ ^ ^2.6 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 1 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~-135 0 positioned ^ ^ ^2.6 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 1 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~135 0 positioned ^ ^ ^2.6 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 0 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~90 0 positioned ^ ^ ^2.6 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 0 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~-90 0 positioned ^ ^ ^2.6 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 1 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~-90 0 positioned ^ ^ ^2.6 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 1 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~90 0 positioned ^ ^ ^2.6 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 0 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~45 0 positioned ^ ^ ^2.6 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 0 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~-45 0 positioned ^ ^ ^2.6 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 1 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~-45 0 positioned ^ ^ ^2.6 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 1 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~45 0 positioned ^ ^ ^2.6 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~0 0 positioned ^ ^ ^2.8 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~180 0 positioned ^ ^ ^3.4 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 0 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~135 0 positioned ^ ^ ^3.4 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 0 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~-135 0 positioned ^ ^ ^3.4 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 1 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~-135 0 positioned ^ ^ ^3.4 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 1 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~135 0 positioned ^ ^ ^3.4 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 0 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~90 0 positioned ^ ^ ^3.4 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 0 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~-90 0 positioned ^ ^ ^3.4 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 1 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~-90 0 positioned ^ ^ ^3.4 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 1 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~90 0 positioned ^ ^ ^3.4 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 0 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~45 0 positioned ^ ^ ^3.4 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 0 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~-45 0 positioned ^ ^ ^3.4 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 1 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~-45 0 positioned ^ ^ ^3.4 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute if score #cl_r tk matches 1 at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~45 0 positioned ^ ^ ^3.4 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ rotated as @e[tag=rlk_body,limit=1] rotated ~0 0 positioned ^ ^ ^3.6 if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
