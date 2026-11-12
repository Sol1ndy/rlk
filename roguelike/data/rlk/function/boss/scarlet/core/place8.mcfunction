# @s = body: to a floor point 8 b from the player (on the player -> her line, else pulled toward the axis
# until mv/ok passes), facing the player.
kill @e[type=minecraft:marker,tag=rlk_hr_pl8]
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^8 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_pl8"]}
scoreboard players set #t4 hr 0
execute as @e[type=minecraft:marker,tag=rlk_hr_pl8,limit=1] at @s run function rlk:boss/scarlet/core/clamp
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_pl8,limit=1] run tp @s ~ ~ ~
kill @e[type=minecraft:marker,tag=rlk_hr_pl8]
function rlk:mboss/mv/face
execute at @s rotated as @s rotated ~ 0 run function rlk:boss/scarlet/rig/follow_now
