# B2 화염 날개의 습격 (STUB; clip wing_barrage: swings [0, 26, 64, 89], 5 crescents each landing +14..+18).
function rlk:mboss/butterfly/rig_stub/face/player
function rlk:mboss/butterfly/u/lockp
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12l]
tag @e[type=minecraft:marker,tag=rlk_mb_bf_lock] add rlk_mb_bf_p12l
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12l] remove rlk_mb_bf_lock
function rlk:mboss/grp_new
particle minecraft:flame ^ ^3.0 ^ 1.8 0.8 0.5 0.04 14 force @a[tag=player]
playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.6 1.6 0.2
playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 0.6 1.2 0.2
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] facing entity @s feet rotated ~ 0 positioned ^-2.2 ^ ^ positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:10,tell:14,dmg:50}
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] facing entity @s feet rotated ~ 0 positioned ^-1.1 ^ ^ positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:10,tell:15,dmg:50}
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^ positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:10,tell:16,dmg:50}
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] facing entity @s feet rotated ~ 0 positioned ^1.1 ^ ^ positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:10,tell:17,dmg:50}
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] facing entity @s feet rotated ~ 0 positioned ^2.2 ^ ^ positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:10,tell:18,dmg:50}
