# @s = body (clip tick 42). U = the player now; D = 5.5 b from U, 75 deg round it from her side
# (random side, the other one when outside the arena, then clamped); a 7.0 x 2.2 b lane from D
# through U strikes at 58 (knockback 4 along it); she flies to D over 12 t.
kill @e[type=minecraft:marker,tag=rlk_mb_gd_p1u,limit=1]
kill @e[type=minecraft:marker,tag=rlk_mb_gd_p1d,limit=1]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p1","rlk_mb_gd_p1u"]}
execute store result score #gp1S mb run random value 0..1
execute if score #gp1S mb matches 0 at @e[type=minecraft:marker,tag=rlk_mb_gd_p1u,limit=1] facing entity @s feet rotated ~75 0 positioned ^ ^ ^5.5 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p1","rlk_mb_gd_p1d"]}
execute if score #gp1S mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_gd_p1u,limit=1] facing entity @s feet rotated ~-75 0 positioned ^ ^ ^5.5 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p1","rlk_mb_gd_p1d"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_gd_p1d,limit=1] at @s unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..18.5] run function rlk:mboss/guardian/p/thrust/flip
execute as @e[type=minecraft:marker,tag=rlk_mb_gd_p1d,limit=1] run function rlk:mboss/mv/clamp
execute as @e[type=minecraft:marker,tag=rlk_mb_gd_p1d,limit=1] at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_gd_p1u,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 12
scoreboard players set #hzLinger mb 4
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p1d,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p1d,limit=1] run function rlk:mboss/hz/line {len:70,w:22,tell:16,dmg:115}
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_gd_p1d,limit=1] run function rlk:mboss/mv/glide {t:12}
