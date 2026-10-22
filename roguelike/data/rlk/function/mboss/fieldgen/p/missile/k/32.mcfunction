# missile clock 32
execute at @s rotated as @s rotated ~ 0 positioned ^2.806 ^4.875 ^-1.162 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p4","rlk_mb_fg_p4m","rlk_mb_fg_p4i6","rlk_mb_fg_pnew"],Rotation:[0f,-90f],teleport_duration:7}
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] run function rlk:mboss/fieldgen/fx/prop/missile
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbT 0
scoreboard players operation @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbS = #mbGrp mb
tag @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] remove rlk_mb_fg_pnew
execute at @s rotated as @s rotated ~ 0 positioned ^2.806 ^4.875 ^-1.162 run function rlk:mboss/fieldgen/fx/p/missile_launch
execute at @s rotated as @s rotated ~ 0 positioned ^2.806 ^4.875 ^-1.162 run function rlk:mboss/fieldgen/fx/snd/missile_launch
