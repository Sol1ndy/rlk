# laser clock 24
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^2.38 ^2.93 rotated ~ 41 run function rlk:mboss/fieldgen/fx/p/laser_fire {len:3.74}
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3g,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^2.38 ^2.93 rotated ~ 41 run function rlk:mboss/fieldgen/fx/p/laser_fire {len:3.74}
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^0.05 ^5.58 run function rlk:mboss/fieldgen/fx/p/laser_spot
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3g,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^0.05 ^5.58 run function rlk:mboss/fieldgen/fx/p/laser_spot
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/snd/laser_fire
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] run function rlk:mboss/hz/resize {r:28,r0:0,w:10}
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3g,limit=1] run function rlk:mboss/hz/resize {r:28,r0:0,w:10}
kill @e[type=minecraft:item_display,tag=rlk_mb_fg_p3b]
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^2.38 ^2.93 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p3","rlk_mb_fg_p3b","rlk_mb_fg_p3be","rlk_mb_fg_pnew"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] run function rlk:mboss/fieldgen/fx/prop/laser_core
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] run data merge entity @s {transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.45f,3.74f,0.45f]}}
tag @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] remove rlk_mb_fg_pnew
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^2.38 ^2.93 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p3","rlk_mb_fg_p3b","rlk_mb_fg_p3be","rlk_mb_fg_pnew"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] run function rlk:mboss/fieldgen/fx/prop/laser_glow
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] run data merge entity @s {transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1f,3.74f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] remove rlk_mb_fg_pnew
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p3be] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] rotated ~ 0 positioned ^ ^2.38 ^2.93 run tp @s ~ ~ ~ ~ -49
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3g,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^2.38 ^2.93 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p3","rlk_mb_fg_p3b","rlk_mb_fg_p3bg","rlk_mb_fg_pnew"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] run function rlk:mboss/fieldgen/fx/prop/laser_core
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] run data merge entity @s {transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.45f,3.74f,0.45f]}}
tag @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] remove rlk_mb_fg_pnew
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3g,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^2.38 ^2.93 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p3","rlk_mb_fg_p3b","rlk_mb_fg_p3bg","rlk_mb_fg_pnew"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] run function rlk:mboss/fieldgen/fx/prop/laser_glow
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] run data merge entity @s {transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1f,3.74f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] remove rlk_mb_fg_pnew
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p3bg] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_fg_p3g,limit=1] rotated ~ 0 positioned ^ ^2.38 ^2.93 run tp @s ~ ~ ~ ~ -49
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^0.05 ^5.58 run function rlk:mboss/fieldgen/fx/snd/laser_loop
