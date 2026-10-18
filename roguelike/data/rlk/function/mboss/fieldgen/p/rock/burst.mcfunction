# One floor burst at the walker (10 t telegraph, jumpable), its slab (hidden until the strike), then the
# walker steps 2.5 b toward the player (onto the player when closer).
scoreboard players add #fq6K mb 1
scoreboard players set #hzKB mb 4
scoreboard players set #hzVis mb 61
scoreboard players set #hzY1 mb 12
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p6w,limit=1] run function rlk:mboss/hz/disc {r:18,tell:10,dmg:130}
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p6w,limit=1] run summon minecraft:item_display ~ ~0.45 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p6","rlk_mb_fg_p6s","rlk_mb_fg_pnew"],teleport_duration:15,brightness:{block:12,sky:15},item:{id:"minecraft:tuff",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]}}
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbT -10
scoreboard players operation @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbS = #fq6K mb
tag @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] remove rlk_mb_fg_pnew
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p6w,limit=1] at @e[tag=rlk_body,limit=1] if entity @s[distance=..2.5] run return run tp @s ~ 201 ~
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p6w,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^2.5 run tp @s ~ 201 ~
