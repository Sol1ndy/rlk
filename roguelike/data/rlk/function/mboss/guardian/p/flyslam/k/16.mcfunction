# flyslam clip tick 16
execute at @s rotated as @s rotated ~ 0 positioned ^-1.034 ^0.25 ^0.182 run particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.567 ^0.721 ^0.841 run particle minecraft:dust{color:[0.976f,0.91f,0.647f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^0.203 ^1.193 ^0.957 run particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^0.8 ^1.664 ^0.5 run particle minecraft:dust{color:[0.976f,0.91f,0.647f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^0.88 ^2.136 ^-0.219 run particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^0.436 ^2.607 ^-0.755 run particle minecraft:dust{color:[0.976f,0.91f,0.647f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.23 ^3.079 ^-0.803 run particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.706 ^3.55 ^-0.376 run particle minecraft:dust{color:[0.976f,0.91f,0.647f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^1.034 ^0.25 ^-0.182 run particle minecraft:dust{color:[0.976f,0.91f,0.647f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^0.567 ^0.721 ^-0.841 run particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.203 ^1.193 ^-0.957 run particle minecraft:dust{color:[0.976f,0.91f,0.647f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.8 ^1.664 ^-0.5 run particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.88 ^2.136 ^0.219 run particle minecraft:dust{color:[0.976f,0.91f,0.647f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.436 ^2.607 ^0.755 run particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^0.23 ^3.079 ^0.803 run particle minecraft:dust{color:[0.976f,0.91f,0.647f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^0.706 ^3.55 ^0.376 run particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p5","rlk_mb_gd_p5b","rlk_mb_gd_p5b62"],block_state:{id:"minecraft:yellow_stained_glass"},brightness:{sky:15,block:15},view_range:1.6f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.31f,0f,-0.31f],left_rotation:[0f,0f,0f,1f],scale:[0.62f,0.2f,0.62f],right_rotation:[0f,0f,0f,1f]}}
execute at @s run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p5","rlk_mb_gd_p5b","rlk_mb_gd_p5b16"],block_state:{id:"minecraft:white_concrete"},brightness:{sky:15,block:15},view_range:1.6f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-0.08f,0f,-0.08f],left_rotation:[0f,0f,0f,1f],scale:[0.16f,0.2f,0.16f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"crescent",pos:"^ ^1.5 ^",rot:"~ ~",bb:"fixed",roll:0,spin:160,s0:2.4,s1:3.2,move:"0f,0f,0f",life:5,fade:2}
execute at @s rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"crescent",pos:"^ ^2.7 ^",rot:"~ ~",bb:"fixed",roll:180,spin:150,s0:2,s1:2.9,move:"0f,0f,0f",life:5,fade:2}
particle minecraft:dust{color:[1f,0.96f,0.75f],scale:1.6} ~ ~3 ~ 0.15 3 0.15 0 30 force @a[tag=player]
playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.7 1.6 0.3
