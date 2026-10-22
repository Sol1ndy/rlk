# @s = body (t46): the flat shot: the light band from the muzzle toward L, the launch flash.
execute at @s rotated as @s positioned ^0 ^2.51 ^4.34 facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_p36l,limit=1] feet rotated ~ 0 run function rlk:boss/apep/fx/p/light_band with storage rlk:mboss ap.p36
execute at @s rotated as @s positioned ^0 ^2.51 ^4.34 run function rlk:boss/apep/fx/p/launch_flash
execute at @s run function rlk:boss/apep/fx/snd/q3s_launch
