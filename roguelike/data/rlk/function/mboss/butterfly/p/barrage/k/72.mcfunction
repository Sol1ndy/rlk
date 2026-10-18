# barrage clock 72
# SWING 4: lock L (walk disc), her yaw S -> L, the 5 targets (along the aim), each
# crescent's dive time from its distance and its Pyro ground marker (fill = landing tick), the volley group of
# the swing, the flame sheet and the launch roar.
function rlk:mboss/butterfly/rig/face/player
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12l]
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12ts4]
function rlk:mboss/butterfly/wx/u/lockw
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12l]
tag @e[type=minecraft:marker,tag=rlk_mb_bf_lock] add rlk_mb_bf_p12l
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12l] add rlk_mb_bf_kept
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12l] remove rlk_mb_bf_lock
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rlk:mboss/grp_new
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^0 ^ ^0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t40","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t40] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t40] add rlk_mb_bf_p12ts4
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t40,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^0 ^5.321 ^4.857 run function rlk:mboss/butterfly/p/barrage/dive40
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^0 ^ ^1.8 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t41","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t41] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t41] add rlk_mb_bf_p12ts4
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t41,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^2.429 ^5.321 ^4.207 run function rlk:mboss/butterfly/p/barrage/dive41
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^0 ^ ^-1.8 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t42","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t42] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t42] add rlk_mb_bf_p12ts4
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t42,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^-2.429 ^5.321 ^4.207 run function rlk:mboss/butterfly/p/barrage/dive42
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^0 ^ ^3.6 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t43","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t43] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t43] add rlk_mb_bf_p12ts4
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t43,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^4.207 ^5.321 ^2.429 run function rlk:mboss/butterfly/p/barrage/dive43
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12l,limit=1] rotated as @s rotated ~ 0 positioned ^0 ^ ^-3.6 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12t44","rlk_mb_bf_kept"]}
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t44] add rlk_mb_bf_p12t
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12t44] add rlk_mb_bf_p12ts4
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t44,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_w
execute rotated as @s rotated ~ 0 positioned ^-4.207 ^5.321 ^2.429 run function rlk:mboss/butterfly/p/barrage/dive44
execute rotated as @s rotated ~ 0 positioned ~ ~3.0 ~ run function rlk:mboss/butterfly/fx/p/fire_swing
execute rotated as @s rotated ~ 0 run particle minecraft:flame ^ ^3.0 ^1.5 2.5 0.6 1 0.05 20 force @a[tag=player]
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"^2.2 ^3.4 ^0.6",rot:"~90 0",bb:"fixed",roll:0,spin:0,s0:3,s1:4.5,move:"0f,0f,0f",life:3,fade:1,col:16513529}
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"^-2.2 ^2.6 ^0.6",rot:"~90 0",bb:"fixed",roll:0,spin:0,s0:3,s1:4.5,move:"0f,0f,0f",life:3,fade:1,col:16513529}
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"^0 ^4.4 ^0.2",rot:"~90 0",bb:"fixed",roll:0,spin:0,s0:3,s1:4.5,move:"0f,0f,0f",life:3,fade:1,col:16513529}
function rlk:mboss/butterfly/fx/snd/fire_cres_launch
playsound minecraft:entity.ghast.shoot hostile @a[tag=player] ~ ~ ~ 0.4 1.2 0.13
# the pattern bar: B2 ends after its last landing (+1), later than the clip's 95 when a far dive is slow
scoreboard players set #bp12E mb 0
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t] run scoreboard players operation #bp12E mb > @s mbT
scoreboard players add #bp12E mb 1
scoreboard players operation #bfPLen mb > #bp12E mb
