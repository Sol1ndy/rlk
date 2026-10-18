# @s = body, at it, rotated toward the player's feet (pitch 0): the route end E (24.75 b along the line, pulled
# back along it into r 16.5) and the predictor P at the body with the route yaw. Older markers go first.
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p1p]
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p1e]
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p1d]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p1","rlk_mb_fg_p1p"]}
tp @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] ~ ~ ~ ~ 0
execute positioned ^ ^ ^24.75 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p1","rlk_mb_fg_p1e"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p1e,limit=1] at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set #fq1N mb 0
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p1e,limit=1] at @s run function rlk:mboss/fieldgen/p/bomb/pull
