# @s = body: the skid after the stop (charge_stop 0..8): a decelerating slide inside the charge disc and a
# turn of <= 3 deg/t toward the player for 9 t; no body push.
scoreboard players add #aq3K mb 1
execute if score #aq3K mb matches 2 at @s rotated as @s rotated ~ 0 positioned ^ ^ ^0.5 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..12,limit=1] run tp @s ~ ~ ~
execute if score #aq3K mb matches 3 at @s rotated as @s rotated ~ 0 positioned ^ ^ ^0.4 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..12,limit=1] run tp @s ~ ~ ~
execute if score #aq3K mb matches 4 at @s rotated as @s rotated ~ 0 positioned ^ ^ ^0.3 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..12,limit=1] run tp @s ~ ~ ~
execute if score #aq3K mb matches 5 at @s rotated as @s rotated ~ 0 positioned ^ ^ ^0.2 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..12,limit=1] run tp @s ~ ~ ~
execute if score #aq3K mb matches 6 at @s rotated as @s rotated ~ 0 positioned ^ ^ ^0.1 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..12,limit=1] run tp @s ~ ~ ~
execute if score #aq3K mb matches 2..10 run function rlk:mboss/mv/turn {max:3}
execute if score #aq3K mb matches ..9 run scoreboard players set #azNoPush mb 1
execute if score #aq3K mb matches 11.. run scoreboard players set #aq3K mb 0
