# one dash tell (7 t): lock the yaw (zig-zag +12 / -12 / +12 deg off the body), walk the landing now
scoreboard players set @s cmT 7
execute if score @s cmN matches 1 facing entity @e[tag=rlk_body,limit=1] feet rotated ~-12 0 run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0
execute unless score @s cmN matches 1 facing entity @e[tag=rlk_body,limit=1] feet rotated ~12 0 run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0
execute store result score @s cmYaw run data get entity @e[tag=rlk_cmrot,limit=1] Rotation[0] 100
tag @s add rlk_c2_fix
# length: about 1.5 b past the body, 3..6 b (0.5 b steps)
scoreboard players set #wN tmp 12
execute if entity @e[tag=rlk_body,distance=..3.5] run scoreboard players set #wN tmp 10
execute if entity @e[tag=rlk_body,distance=..2.5] run scoreboard players set #wN tmp 8
execute if entity @e[tag=rlk_body,distance=..1.5] run scoreboard players set #wN tmp 6
execute as @e[tag=rlk_kr_dst] if score @s cmId = #cid tmp run kill @s
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_kr_dst","rlk_c2cur","rlk_cmlink","rlk_cmsync"]}
scoreboard players operation @e[tag=rlk_c2cur] cmId = #cid tmp
execute rotated as @e[tag=rlk_cmrot,limit=1] as @e[tag=rlk_c2cur,limit=1] run tp @s ~ ~ ~ ~ 0
execute as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/kr/lib/walk
scoreboard players operation @s cmD = #wK tmp
tag @e[tag=rlk_c2cur] remove rlk_c2cur
# tell: the blade flares purple + a bright ring
particle minecraft:electric_spark ^-0.45 ^1.3 ^0.5 0.12 0.35 0.12 0.05 12
particle minecraft:end_rod ^-0.45 ^1.7 ^0.5 0 0 0 0 1
playsound minecraft:item.trident.return master @a ~ ~ ~ 1 1.7
