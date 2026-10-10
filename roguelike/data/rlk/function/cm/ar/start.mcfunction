scoreboard players set @s cmS 1
scoreboard players set @s cmAR 0
scoreboard players operation @s cmT = #cmW_ar tmp
function rlk:cm/ch_begin
execute positioned ~ ~1.45 ~ run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_cmlink","rlk_cmline","rlk_cmnew2"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:red_concrete"},transformation:{translation:[-0.03f,-0.03f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.06f,0.06f,0.1f]}}
scoreboard players operation @e[tag=rlk_cmnew2] cmId = #cid tmp
tag @e[tag=rlk_cmnew2] remove rlk_cmnew2
execute unless score #k105 snd matches 1 run function rlk:snd/f112
