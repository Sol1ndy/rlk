# Burst 6 decal (@s = body): the arc point 26 deg off the bearing to the player (side #fq12S), at the
# player's distance from the device (2.5-18 b), in the walk disc; the quiet hazard + the violet decal; the
# slab, hidden until the strike.
function rlk:mboss/mv/dist
scoreboard players operation #fq12D mb = #mbDist mb
execute if score #fq12D mb matches ..24 run scoreboard players set #fq12D mb 25
execute if score #fq12D mb matches 181.. run scoreboard players set #fq12D mb 180
execute store result storage rlk:mboss fg.f2.d double 0.1 run scoreboard players get #fq12D mb
execute if score #fq12S mb matches 1 run data modify storage rlk:mboss fg.f2.a set value 26
execute unless score #fq12S mb matches 1 run data modify storage rlk:mboss fg.f2.a set value -26
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p12w]
function rlk:mboss/fieldgen/p/frock/place with storage rlk:mboss fg.f2
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p12w,limit=1] run function rlk:mboss/fieldgen/u/clamp_w
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 121
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 12
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p12w,limit=1] run function rlk:mboss/hz/disc {r:18,tell:10,dmg:70}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_fg_p12z
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p12w,limit=1] rotated ~ 0 run function rlk:mboss/fieldgen/fx/tele/disc {r:18,tell:10,el:9,hold:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p12w,limit=1] run playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.3 1.4 0.1
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p12w,limit=1] run summon minecraft:item_display ~ ~0.45 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p12","rlk_mb_fg_p12s","rlk_mb_fg_pnew"],teleport_duration:12}
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] run function rlk:mboss/fieldgen/fx/prop/slab
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew,limit=1] {transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]}}
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbS 6
tag @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] remove rlk_mb_fg_pnew
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p12w]
