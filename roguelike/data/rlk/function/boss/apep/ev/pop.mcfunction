# The floor popup "…" above the head, at most once per 10 t.
scoreboard players operation #apX mb = #apFc mb
scoreboard players operation #apX mb -= #apPopC mb
execute if score #apX mb matches ..9 run return 0
scoreboard players operation #apPopC mb = #apFc mb
execute at @s run summon minecraft:text_display ~ ~4.6 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pop"],billboard:"center",text:{text:"…",color:"#E9E2B8"},background:0,see_through:1b,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.6f,1.6f,1.6f]}}
scoreboard players set @e[type=minecraft:text_display,tag=rlk_mb_ap_pop] apT 16
