# barrage clock 4
# SWING 1: lock L (walk disc), her yaw S -> L, the 5 targets (across the aim), each
# crescent's dive time from its distance and its Pyro ground marker (fill = landing tick), the volley group of
# the swing, the flame sheet and the launch roar.
function rlk:mboss/butterfly/rig/face/player
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12l]
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12ts1]
function rlk:mboss/butterfly/wx/u/lockw
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12l]
tag @e[type=minecraft:marker,tag=rlk_mb_bf_lock] add rlk_mb_bf_p12l
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12l] add rlk_mb_bf_kept
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12l] remove rlk_mb_bf_lock
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rlk:mboss/grp_new
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^0 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t10","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t10] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t10] add rlk_mb_bf_p12ts1
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t10,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^0 ^5.321 ^4.857 run function rlk:mboss/butterfly/p/barrage/dive10
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^1.8 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t11","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t11] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t11] add rlk_mb_bf_p12ts1
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t11,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^2.429 ^5.321 ^4.207 run function rlk:mboss/butterfly/p/barrage/dive11
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^-1.8 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t12","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t12] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t12] add rlk_mb_bf_p12ts1
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t12,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^-2.429 ^5.321 ^4.207 run function rlk:mboss/butterfly/p/barrage/dive12
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^3.6 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t13","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t13] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t13] add rlk_mb_bf_p12ts1
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t13,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^4.207 ^5.321 ^2.429 run function rlk:mboss/butterfly/p/barrage/dive13
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^-3.6 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t14","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t14] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t14] add rlk_mb_bf_p12ts1
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t14,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^-4.207 ^5.321 ^2.429 run function rlk:mboss/butterfly/p/barrage/dive14
execute rotated as @s rotated ~ 0 positioned ~ ~3.0 ~ run function rlk:mboss/butterfly/fx/p/fire_swing_d
execute rotated as @s rotated ~ 0 run particle minecraft:flame ^ ^3.0 ^1.5 2.5 0.6 1 0.05 20 force @a[tag=player]
function rlk:mboss/butterfly/fx/snd/fire_cres_launch
playsound minecraft:entity.ghast.shoot hostile @a[tag=player] ~ ~ ~ 0.4 1.2 0.13
