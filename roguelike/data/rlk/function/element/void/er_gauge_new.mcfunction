# 게이지 조각 만들기 (@s = 몹): 띠 · 눈금 · 마름모. 체력 바처럼 몹에 탑승, 화면을 본다
execute on passengers if entity @s[tag=rlk_hb_er] run kill @s
tag @s add rlk_ego
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_hb_er","rlk_hb_ers","rlk_eg_new"],billboard:"center",interpolation_duration:3,brightness:{sky:15,block:15},Glowing:1b,glow_color_override:16727968,block_state:{id:"minecraft:magenta_concrete"},transformation:{translation:[-0.8f,0.165f,0.012f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0.075f,0.02f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_hb_er","rlk_hb_erz","rlk_eg_new"],billboard:"center",interpolation_duration:3,brightness:{sky:15,block:15},block_state:{id:"minecraft:magenta_stained_glass"},transformation:{translation:[-0.8f,0.25f,0.044f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0.13f,0.004f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_hb_er","rlk_hb_ert","rlk_eg_new"],billboard:"center",interpolation_duration:3,brightness:{sky:15,block:15},Glowing:1b,glow_color_override:16727968,block_state:{id:"minecraft:white_concrete"},transformation:{translation:[-0.815f,0.15f,0.05f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.03f,0.29f,0.02f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_hb_er","rlk_hb_erd","rlk_eg_new"],billboard:"center",interpolation_duration:3,brightness:{sky:15,block:15},Glowing:1b,glow_color_override:16727968,block_state:{id:"minecraft:magenta_concrete"},transformation:{translation:[-0.8f,0.2231f,0.06f],left_rotation:[0.0000f,0.0000f,0.3827f,0.9239f],right_rotation:[0f,0f,0f,1f],scale:[0.130f,0.130f,0.02f]}}
execute as @e[tag=rlk_eg_new] run ride @s mount @e[tag=rlk_ego,limit=1]
tag @e[tag=rlk_eg_new] remove rlk_eg_new
tag @s remove rlk_ego
