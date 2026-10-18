# barrage clock 69
# SWING 3: lock L (walk disc), her yaw S -> L, the 5 targets (across the aim) with their
# Pyro ground markers (fill = landing tick), the volley group of the swing, the flame sheet and the launch roar.
function rlk:mboss/butterfly/rig/face/player
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12l]
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12t]
function rlk:mboss/butterfly/wx/u/lockw
tag @e[type=minecraft:marker,tag=rlk_mb_bf_lock] add rlk_mb_bf_p12l
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12l] remove rlk_mb_bf_lock
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rlk:mboss/grp_new
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^0 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t0"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t0] add rlk_mb_bf_p12t
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t0,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12t0,limit=1] run function rlk:mboss/butterfly/fx/tele/disc {r:12,tell:14,el:1,hold:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^1.8 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t1"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t1] add rlk_mb_bf_p12t
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t1,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12t1,limit=1] run function rlk:mboss/butterfly/fx/tele/disc {r:12,tell:15,el:1,hold:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^-1.8 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t2"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t2] add rlk_mb_bf_p12t
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t2,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12t2,limit=1] run function rlk:mboss/butterfly/fx/tele/disc {r:12,tell:16,el:1,hold:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^3.6 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t3"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t3] add rlk_mb_bf_p12t
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t3,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12t3,limit=1] run function rlk:mboss/butterfly/fx/tele/disc {r:12,tell:17,el:1,hold:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^-3.6 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t4"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t4] add rlk_mb_bf_p12t
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t4,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12t4,limit=1] run function rlk:mboss/butterfly/fx/tele/disc {r:12,tell:18,el:1,hold:3}
execute rotated as @s rotated ~ 0 positioned ~ ~3.0 ~ run function rlk:mboss/butterfly/fx/p/fire_swing_d
execute rotated as @s rotated ~ 0 run particle minecraft:flame ^ ^3.0 ^1.5 2.5 0.6 1 0.05 20 force @a[tag=player]
function rlk:mboss/butterfly/fx/snd/fire_cres_launch
playsound minecraft:entity.ghast.shoot hostile @a[tag=player] ~ ~ ~ 0.4 1.2 0.13
