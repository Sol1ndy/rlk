# @s = body, at it, facing the player: the end of the flight line (pulled back along it into r 16.5) and the
# predictor at the body with the locked yaw.
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p1p]
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p1e]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p1","rlk_mb_fg_p1p"]}
execute rotated as @s run tp @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] ~ ~ ~ ~ 0
execute rotated as @s positioned ^ ^ ^24.75 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p1","rlk_mb_fg_p1e"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p1e,limit=1] at @s rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run tp @s ~ ~ ~ ~180 0
scoreboard players set #fq1N mb 0
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p1e,limit=1] at @s run function rlk:mboss/fieldgen/p/bomb/pull
