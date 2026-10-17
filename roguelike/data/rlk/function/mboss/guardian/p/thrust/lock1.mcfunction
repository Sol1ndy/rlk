# @s = body (clip tick 16). T = the player now; C = 6.959 b from T toward her (clamped into
# the arena) = where she coils; a 8.5 x 2.4 b lane from C through T strikes at clip tick 28.
kill @e[type=minecraft:marker,tag=rlk_mb_gd_p1]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p1","rlk_mb_gd_p1t"]}
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p1t,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^6.959 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p1","rlk_mb_gd_p1c"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_gd_p1c,limit=1] run function rlk:mboss/mv/clamp
execute as @e[type=minecraft:marker,tag=rlk_mb_gd_p1c,limit=1] at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_gd_p1t,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 11
scoreboard players set #hzLinger mb 4
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p1c,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p1c,limit=1] run function rlk:mboss/hz/line {len:85,w:24,tell:12,dmg:100}
execute rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p1c,limit=1] run tp @s ~ ~ ~ ~-5.702 0
