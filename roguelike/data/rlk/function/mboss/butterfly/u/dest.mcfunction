# @s = body, at it. Marker rlk_mb_bf_dest on the line toward the player: at most #bfDMax tenths from her,
# stopping #bfDKeep tenths short of the player, never outside the safe disc (0.5 b steps; none fits = at her
# feet). Patterns keep it with tag ... add rlk_mb_bf_p<id>x + tag ... remove rlk_mb_bf_dest (Gen.keep).
kill @e[type=minecraft:marker,tag=rlk_mb_bf_dest]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_dest"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_dest,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players operation #bfDLeft mb = #bfDMax mb
# the distance to the player once: every 0.5 b step straight at her takes 5 tenths off it (review fix perf-3:
# it used to be re-measured, 89 commands, on every step)
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_dest,limit=1] run function rlk:mboss/mv/dist
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_dest,limit=1] at @s run function rlk:mboss/butterfly/u/dest_step
