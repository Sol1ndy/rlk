# A glowing lime moon-dew orb 1.1 b above the floor here (item_display, billboard; rlk_mb_aux: dies with the fight).
summon minecraft:item_display ~ ~1.1 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_dew"],billboard:"center",Glowing:1b,glow_color_override:11985754,brightness:{block:15,sky:15},item:{id:"minecraft:slime_ball",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
scoreboard players add #bfDewN mb 1
particle minecraft:dust{color:[0.898f,0.984f,0.784f],scale:1.3} ~ ~1.1 ~ 0.3 0.3 0.3 0 12 force @a[tag=player]
particle minecraft:end_rod ~ ~1.1 ~ 0.1 0.1 0.1 0.08 8 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~0 ~0.12 ~0.9 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~0.53 ~0.12 ~0.73 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~0.86 ~0.12 ~0.28 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~0.86 ~0.12 ~-0.28 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~0.53 ~0.12 ~-0.73 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~0 ~0.12 ~-0.9 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~-0.53 ~0.12 ~-0.73 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~-0.86 ~0.12 ~-0.28 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~-0.86 ~0.12 ~0.28 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1} ~-0.53 ~0.12 ~0.73 0 0 0 0 1 force @a[tag=player]
execute positioned ^ ^1.1 ^ rotated ~ ~ run function rlk:mboss/butterfly/tc/card {kind:"star",bb:"center",roll:0,spin:60,s0:0.2,s1:1.4,move:"0f,0f,0f",life:9,fade:4,col:11985754,ax:"0f,0f,1f"}
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.7 1.6 0.23
