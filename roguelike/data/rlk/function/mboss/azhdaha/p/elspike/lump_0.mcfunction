# Lump 1 (impact t44): a new hexagram under a player farther than 8 b from the current one; the lock (the
# player's feet), the disc r 3.0 (tell 13), the lump hovering 12 b over the lock.
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p46h,limit=1] unless entity @e[tag=rlk_body,distance=..8,limit=1] run function rlk:mboss/azhdaha/p/elspike/hex_0
execute unless entity @e[type=minecraft:marker,tag=rlk_mb_az_p46h,limit=1] run function rlk:mboss/azhdaha/p/elspike/hex_0
function rlk:mboss/azhdaha/u/lockp
kill @e[type=minecraft:marker,tag=rlk_mb_az_p46l0]
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_p46l0
tag @e[type=minecraft:marker,tag=rlk_mb_az_p46l0] add rlk_mb_az_pat
tag @e[type=minecraft:marker,tag=rlk_mb_az_p46l0] add rlk_mb_az_p46
tag @e[type=minecraft:marker,tag=rlk_mb_az_p46l0] remove rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_p46l0] remove rlk_mb_lock
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 461
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azET mb
scoreboard players operation #pjEl mb = #azET mb
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p46l0,limit=1] run function rlk:mboss/hz/disc {r:30,tell:13,dmg:70}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p46
scoreboard players operation #aq46G mb = #mbGrp mb
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p46l0,limit=1] run summon minecraft:item_display ~ ~12 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p46","rlk_mb_az_p46p0"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p46p0] run function rlk:mboss/azhdaha/fx/prop/elump
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p46l0,limit=1] positioned ~ ~12 ~ run particle minecraft:electric_spark ~ ~ ~ 0.4 0.4 0.4 0.1 6 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p46l0,limit=1] positioned ~ ~12 ~ run playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.7 1.5 0.23
