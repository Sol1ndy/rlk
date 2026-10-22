# [c_rocks] Burst 2/8 (@s = body; strikes 10 t from now): the arc point at the player's distance,
# 77.1 degrees off their bearing on the sweep side, its decal, its waiting slab.
function rlk:mboss/mv/dist
execute if score #mbDist mb matches ..24 run scoreboard players set #mbDist mb 25
execute if score #mbDist mb matches 181.. run scoreboard players set #mbDist mb 180
execute store result storage rlk:mboss fg.rk.d double 0.1 run scoreboard players get #mbDist mb
execute if score #fq6S mb matches 1 run data modify storage rlk:mboss fg.rk.a set value 77.1d
execute unless score #fq6S mb matches 1 run data modify storage rlk:mboss fg.rk.a set value -77.1d
function rlk:mboss/fieldgen/p/rock/rk_place with storage rlk:mboss fg.rk
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 61
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 12
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p6w,limit=1] run function rlk:mboss/hz/disc {r:18,tell:10,dmg:225}
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p6w,limit=1] run playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.3 1.4 0.1
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p6w,limit=1] run summon minecraft:item_display ~ ~0.45 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p6","rlk_mb_fg_p6s","rlk_mb_fg_pnew"],teleport_duration:12,brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] run function rlk:mboss/fieldgen/fx/prop/slab
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] run data merge entity @s {transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]}}
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbT -10
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbS 2
tag @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] remove rlk_mb_fg_pnew
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p6w]
