# barrage clock 24
# SWING 2: lock L (walk disc), her yaw S -> L, the 5 targets (along the aim), each
# crescent's dive time from its distance and its Pyro ground marker (fill = landing tick), the volley group of
# the swing, the flame sheet and the launch roar.
function rlk:mboss/butterfly/rig/face/player
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12l]
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12ts2]
function rlk:mboss/butterfly/wx/u/lockw
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12l]
tag @e[type=minecraft:marker,tag=rlk_mb_bf_lock] add rlk_mb_bf_p12l
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12l] add rlk_mb_bf_kept
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12l] remove rlk_mb_bf_lock
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rlk:mboss/grp_new
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^0 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t20","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t20] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t20] add rlk_mb_bf_p12ts2
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t20,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^0 ^5.321 ^4.857 run function rlk:mboss/butterfly/p/barrage/dive20
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^0 ^ ^1.8 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t21","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t21] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t21] add rlk_mb_bf_p12ts2
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t21,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^2.429 ^5.321 ^4.207 run function rlk:mboss/butterfly/p/barrage/dive21
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^0 ^ ^-1.8 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t22","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t22] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t22] add rlk_mb_bf_p12ts2
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t22,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^-2.429 ^5.321 ^4.207 run function rlk:mboss/butterfly/p/barrage/dive22
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^0 ^ ^3.6 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t23","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t23] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t23] add rlk_mb_bf_p12ts2
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t23,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^4.207 ^5.321 ^2.429 run function rlk:mboss/butterfly/p/barrage/dive23
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^0 ^ ^-3.6 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t24","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t24] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t24] add rlk_mb_bf_p12ts2
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t24,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^-4.207 ^5.321 ^2.429 run function rlk:mboss/butterfly/p/barrage/dive24
execute rotated as @s rotated ~ 0 positioned ~ ~3.0 ~ run function rlk:mboss/butterfly/fx/p/fire_swing
execute rotated as @s rotated ~ 0 run particle minecraft:flame ^ ^3.0 ^1.5 2.5 0.6 1 0.05 20 force @a[tag=player]
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"^2.2 ^3.4 ^0.6",rot:"~90 0",bb:"fixed",roll:0,spin:0,s0:3,s1:4.5,move:"0f,0f,0f",life:3,fade:1,col:16513529}
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"^-2.2 ^2.6 ^0.6",rot:"~90 0",bb:"fixed",roll:0,spin:0,s0:3,s1:4.5,move:"0f,0f,0f",life:3,fade:1,col:16513529}
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"^0 ^4.4 ^0.2",rot:"~90 0",bb:"fixed",roll:0,spin:0,s0:3,s1:4.5,move:"0f,0f,0f",life:3,fade:1,col:16513529}
function rlk:mboss/butterfly/fx/snd/fire_cres_launch
playsound minecraft:entity.ghast.shoot hostile @a[tag=player] ~ ~ ~ 0.4 1.2 0.13
