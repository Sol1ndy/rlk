summon minecraft:block_display ~ ~ ~ {Tags:["rlk_cmp","rlk_cmic","rlk_cmpnew"],teleport_duration:1,brightness:{sky:13,block:13},block_state:{id:"minecraft:packed_ice"},transformation:[0.3943f,-0.2887f,-0.1057f,0.0000f,0.7217f,0.7217f,0.7217f,0.0000f,-0.1057f,-0.2887f,0.3943f,0.0000f,0.0000f,0.0000f,0.0000f,1.0000f]}
scoreboard players operation @e[tag=rlk_cmpnew] cmD = #cmD_icD tmp
scoreboard players operation @e[tag=rlk_cmpnew] cmD2 = #cmD_icB tmp
scoreboard players operation @e[tag=rlk_cmpnew] cmLv = #clv tmp
scoreboard players set @e[tag=rlk_cmpnew] cmEl 4
scoreboard players operation @e[tag=rlk_cmpnew] cmT = #cmW_imH tmp
scoreboard players set @e[tag=rlk_cmpnew] cmV 0
scoreboard players operation @e[tag=rlk_cmpnew] cmId = #cid tmp
scoreboard players add #cmK tmp 1
scoreboard players operation @e[tag=rlk_cmpnew] cmN = #cmK tmp
scoreboard players operation #wdT tmp = #cmW_imH tmp
function rlk:cm/gnd {k:"ic"}
tag @e[tag=rlk_cmpnew] remove rlk_cmpnew
particle minecraft:snowflake ~ ~0.8 ~ 0.3 0.5 0.3 0.03 12
execute unless score #k78 snd matches 1 run function rlk:snd/f84
