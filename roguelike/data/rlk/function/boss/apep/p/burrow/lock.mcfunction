# @s = body (t32, hidden): the lock is fixed: the anchor under it (head on the lock, clamp r 18), facing
# it; the burst disc r 4.2 on the head point, tell 12 (keep row: the shadow is the marker, no ring),
# KB 3 outward, height 0-4, 120 %.
kill @e[type=minecraft:marker,tag=rlk_mb_ap_lock]
function rlk:mboss/mv/lockv {lead:10}
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_ap_lock
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] remove rlk_mb_lock
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p1g]
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^3.13 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p1","rlk_mb_ap_p1g"]}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^3.13 positioned ~ 201 ~ run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p1g,limit=1] ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p1g,limit=1] run function rlk:boss/apep/u/clamp_burst1
function rlk:mboss/mv/stop
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p1g,limit=1] facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1] feet run tp @s ~ 201 ~ ~ 0
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p1b]
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^3.13 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p1","rlk_mb_ap_p1b"]}
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^3.13 positioned ~ 201 ~ run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p1b,limit=1] ~ ~ ~ ~ 0
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 3
scoreboard players set #hzKBDir mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 40
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p1b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p1b,limit=1] run function rlk:mboss/hz/disc {r:42,tell:12,dmg:120}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p1
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p1b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p1b,limit=1] run function rlk:boss/apep/fx/snd/p1_ring
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p1g]
