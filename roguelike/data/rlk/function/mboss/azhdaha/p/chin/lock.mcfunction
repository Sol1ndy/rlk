# @s = body (t10): lock the impact point (plan 5 P1): marker rlk_mb_az_p1i, rotated along the crack line
# (anchor -> impact). mv/local gives the player in the anchor frame (mb).
kill @e[type=minecraft:marker,tag=rlk_mb_az_p1i]
summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p1","rlk_mb_az_p1i"]}
function rlk:mboss/mv/local
scoreboard players set #aq1C mb 0
scoreboard players operation #aq1S mb = #mbLs mb
scoreboard players set #aq1K mb -1
execute if score #aq1S mb matches ..-1 run scoreboard players operation #aq1S mb *= #aq1K mb
scoreboard players set #aq1K mb 1000
scoreboard players operation #aq1S mb *= #aq1K mb
scoreboard players operation #aq1T mb = #mbLf mb
scoreboard players set #aq1K mb 577
scoreboard players operation #aq1T mb *= #aq1K mb
# inside the cone: f >= 1 b and |s| <= f tan 30
execute if score #mbLf mb matches 1000.. if score #aq1S mb <= #aq1T mb run scoreboard players set #aq1C mb 1
# the distance: d ~ f + s^2 / 2f in the cone (1 % at 30 degrees), f on the axis; clamped 5.5 .. 7.5 b
scoreboard players operation #aq1D mb = #mbLf mb
execute if score #aq1C mb matches 1 run function rlk:mboss/azhdaha/p/chin/dist
execute if score #aq1D mb matches ..5500 run scoreboard players set #aq1D mb 5500
execute if score #aq1D mb matches 7500.. run scoreboard players set #aq1D mb 7500
scoreboard players remove #aq1D mb 5500
execute if score #aq1C mb matches 1 as @e[type=minecraft:marker,tag=rlk_mb_az_p1i,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
execute if score #aq1C mb matches 0 as @e[type=minecraft:marker,tag=rlk_mb_az_p1i,limit=1] at @s rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p1i,limit=1] at @s rotated as @s run tp @s ^ ^ ^5.5
execute if score #aq1D mb matches 1024.. as @e[type=minecraft:marker,tag=rlk_mb_az_p1i,limit=1] at @s rotated as @s run tp @s ^ ^ ^1.024
execute if score #aq1D mb matches 1024.. run scoreboard players remove #aq1D mb 1024
execute if score #aq1D mb matches 512.. as @e[type=minecraft:marker,tag=rlk_mb_az_p1i,limit=1] at @s rotated as @s run tp @s ^ ^ ^0.512
execute if score #aq1D mb matches 512.. run scoreboard players remove #aq1D mb 512
execute if score #aq1D mb matches 256.. as @e[type=minecraft:marker,tag=rlk_mb_az_p1i,limit=1] at @s rotated as @s run tp @s ^ ^ ^0.256
execute if score #aq1D mb matches 256.. run scoreboard players remove #aq1D mb 256
execute if score #aq1D mb matches 128.. as @e[type=minecraft:marker,tag=rlk_mb_az_p1i,limit=1] at @s rotated as @s run tp @s ^ ^ ^0.128
execute if score #aq1D mb matches 128.. run scoreboard players remove #aq1D mb 128
execute if score #aq1D mb matches 64.. as @e[type=minecraft:marker,tag=rlk_mb_az_p1i,limit=1] at @s rotated as @s run tp @s ^ ^ ^0.064
execute if score #aq1D mb matches 64.. run scoreboard players remove #aq1D mb 64
execute if score #aq1D mb matches 32.. as @e[type=minecraft:marker,tag=rlk_mb_az_p1i,limit=1] at @s rotated as @s run tp @s ^ ^ ^0.032
execute if score #aq1D mb matches 32.. run scoreboard players remove #aq1D mb 32
execute if score #aq1D mb matches 16.. as @e[type=minecraft:marker,tag=rlk_mb_az_p1i,limit=1] at @s rotated as @s run tp @s ^ ^ ^0.016
execute if score #aq1D mb matches 16.. run scoreboard players remove #aq1D mb 16
execute if score #aq1D mb matches 8.. as @e[type=minecraft:marker,tag=rlk_mb_az_p1i,limit=1] at @s rotated as @s run tp @s ^ ^ ^0.008
execute if score #aq1D mb matches 8.. run scoreboard players remove #aq1D mb 8
