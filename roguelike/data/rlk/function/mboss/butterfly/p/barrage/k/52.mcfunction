# barrage clock 52
# SWING 3: lock L (walk disc), her yaw S -> L, the 5 targets (across the aim), each
# crescent's dive time from its distance and its Pyro ground marker (fill = landing tick), the volley group of
# the swing, the flame sheet and the launch roar.
function rlk:mboss/butterfly/rig/face/player
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12l]
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12ts3]
function rlk:mboss/butterfly/wx/u/lockw
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12l]
tag @e[type=minecraft:marker,tag=rlk_mb_bf_lock] add rlk_mb_bf_p12l
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12l] add rlk_mb_bf_kept
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12l] remove rlk_mb_bf_lock
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rlk:mboss/grp_new
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^0 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t30","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t30] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t30] add rlk_mb_bf_p12ts3
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t30,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^0 ^5.321 ^4.857 run function rlk:mboss/butterfly/p/barrage/dive30
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^1.8 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t31","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t31] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t31] add rlk_mb_bf_p12ts3
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t31,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^2.429 ^5.321 ^4.207 run function rlk:mboss/butterfly/p/barrage/dive31
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^-1.8 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t32","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t32] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t32] add rlk_mb_bf_p12ts3
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t32,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^-2.429 ^5.321 ^4.207 run function rlk:mboss/butterfly/p/barrage/dive32
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^3.6 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t33","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t33] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t33] add rlk_mb_bf_p12ts3
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t33,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^4.207 ^5.321 ^2.429 run function rlk:mboss/butterfly/p/barrage/dive33
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^-3.6 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t34","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t34] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t34] add rlk_mb_bf_p12ts3
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t34,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^-4.207 ^5.321 ^2.429 run function rlk:mboss/butterfly/p/barrage/dive34
execute rotated as @s rotated ~ 0 positioned ~ ~3.0 ~ run function rlk:mboss/butterfly/fx/p/fire_swing_d
execute rotated as @s rotated ~ 0 run particle minecraft:flame ^ ^3.0 ^1.5 2.5 0.6 1 0.05 20 force @a[tag=player]
function rlk:mboss/butterfly/fx/snd/fire_cres_launch
playsound minecraft:entity.ghast.shoot hostile @a[tag=player] ~ ~ ~ 0.4 1.2 0.13
