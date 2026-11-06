# @s = body. Spin the star visual; a broken star (rlk_mb_broken from aux/take) is removed and hurts the boss.
execute as @e[tag=rlk_mb_proto_starv] at @s run tp @s ~ ~ ~ ~6 0
execute if entity @e[tag=rlk_mb_proto_star,tag=rlk_mb_broken,limit=1] run function rlk:mboss/proto/star_break
